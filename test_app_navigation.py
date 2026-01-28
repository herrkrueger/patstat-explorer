#!/usr/bin/env python3
"""Tests for app navigation state and functions (Story 1.1 Task 1).

Uses a test-friendly approach by directly testing the navigation logic
with streamlit mocked at the module level.
"""

import pytest
import sys
from unittest.mock import MagicMock, patch


class MockSessionState(dict):
    """Mock Streamlit session state that behaves like a dict with attribute access."""

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


# Create mock streamlit before importing app
mock_st = MagicMock()
mock_st.session_state = MockSessionState()
mock_st.rerun = MagicMock()
mock_st.set_page_config = MagicMock()
mock_st.title = MagicMock()
mock_st.caption = MagicMock()
mock_st.cache_resource = lambda f: f
mock_st.cache_data = lambda **kwargs: lambda f: f

# Patch before imports
sys.modules['streamlit'] = mock_st

# Now we can import from app
from app import init_session_state, go_to_landing, go_to_detail, render_landing_page, render_query_list, render_detail_page, CATEGORIES
from queries_bq import QUERIES


@pytest.fixture(autouse=True)
def reset_session_state():
    """Reset session state and mock before each test."""
    mock_st.session_state.clear()
    mock_st.rerun.reset_mock()
    yield


class TestSessionStateInitialization:
    """Test session state initialization for navigation (Subtasks 1.1-1.3)."""

    def test_init_session_state_sets_current_page_to_landing(self):
        """1.1: current_page defaults to 'landing'."""
        init_session_state()

        assert mock_st.session_state['current_page'] == 'landing'

    def test_init_session_state_sets_selected_query_to_none(self):
        """1.2: selected_query defaults to None."""
        init_session_state()

        assert mock_st.session_state['selected_query'] is None

    def test_init_session_state_sets_selected_category_to_none(self):
        """1.3: selected_category defaults to None."""
        init_session_state()

        assert mock_st.session_state['selected_category'] is None

    def test_init_session_state_preserves_existing_values(self):
        """Init should not overwrite existing session state values."""
        mock_st.session_state['current_page'] = 'detail'
        mock_st.session_state['selected_query'] = 'Q01'
        mock_st.session_state['selected_category'] = 'Trends'

        init_session_state()

        assert mock_st.session_state['current_page'] == 'detail'
        assert mock_st.session_state['selected_query'] == 'Q01'
        assert mock_st.session_state['selected_category'] == 'Trends'


class TestNavigationFunctions:
    """Test navigation functions (Subtask 1.4)."""

    def test_go_to_landing_sets_current_page(self):
        """go_to_landing() sets current_page to 'landing'."""
        mock_st.session_state['current_page'] = 'detail'

        go_to_landing()

        assert mock_st.session_state['current_page'] == 'landing'

    def test_go_to_landing_clears_selected_query(self):
        """go_to_landing() clears selected_query."""
        mock_st.session_state['selected_query'] = 'Q01'

        go_to_landing()

        assert mock_st.session_state['selected_query'] is None

    def test_go_to_landing_preserves_selected_category(self):
        """go_to_landing() preserves selected_category for state restoration (AC #5)."""
        mock_st.session_state['selected_category'] = 'Competitors'

        go_to_landing()

        assert mock_st.session_state['selected_category'] == 'Competitors'

    def test_go_to_landing_calls_rerun(self):
        """go_to_landing() triggers st.rerun()."""
        go_to_landing()

        mock_st.rerun.assert_called_once()

    def test_go_to_detail_sets_current_page(self):
        """go_to_detail() sets current_page to 'detail'."""
        mock_st.session_state['current_page'] = 'landing'

        go_to_detail('Q01')

        assert mock_st.session_state['current_page'] == 'detail'

    def test_go_to_detail_sets_selected_query(self):
        """go_to_detail() sets selected_query to the provided query_id."""
        go_to_detail('Q05')

        assert mock_st.session_state['selected_query'] == 'Q05'

    def test_go_to_detail_calls_rerun(self):
        """go_to_detail() triggers st.rerun()."""
        go_to_detail('Q01')

        mock_st.rerun.assert_called_once()

    def test_go_to_detail_validates_query_id(self):
        """go_to_detail() should not navigate for invalid query_id (M2 fix)."""
        mock_st.rerun.reset_mock()
        mock_st.session_state['current_page'] = 'landing'

        go_to_detail('INVALID_QUERY')

        # Should NOT call rerun for invalid query
        mock_st.rerun.assert_not_called()
        # Should remain on landing page
        assert mock_st.session_state.get('current_page') == 'landing'


class TestLandingPage:
    """Test landing page layout (Task 2)."""

    def test_render_landing_page_exists(self):
        """2.2: render_landing_page function should exist."""
        assert callable(render_landing_page)

    def test_render_landing_page_displays_title(self):
        """2.3: Landing page shows 'What do you want to know?' title."""
        # Reset mocks for this test
        mock_st.pills = MagicMock(return_value=None)
        mock_st.header = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.divider = MagicMock()
        mock_st.info = MagicMock()
        mock_st.button = MagicMock(return_value=False)

        # Create mock columns that support context manager
        mock_col = MagicMock()
        mock_col.__enter__ = MagicMock(return_value=mock_col)
        mock_col.__exit__ = MagicMock(return_value=None)
        mock_st.columns = MagicMock(return_value=[mock_col] * 5)

        render_landing_page()

        # Check that header was called with the expected title
        mock_st.header.assert_any_call("What do you want to know?")

    def test_category_pills_options(self):
        """2.4: Category pills include all required categories."""
        expected_categories = ["Competitors", "Trends", "Regional", "Technology"]
        assert CATEGORIES == expected_categories


class TestQueryCategories:
    """Test query category assignments (Task 3)."""

    def test_all_queries_have_category_field(self):
        """3.1: Every query in QUERIES dict has a 'category' field."""
        for query_id, query_info in QUERIES.items():
            assert 'category' in query_info, f"Query {query_id} missing 'category' field"

    def test_all_categories_are_valid(self):
        """3.2: All query categories are one of the defined categories."""
        valid_categories = {"Competitors", "Trends", "Regional", "Technology"}
        for query_id, query_info in QUERIES.items():
            assert query_info['category'] in valid_categories, \
                f"Query {query_id} has invalid category: {query_info['category']}"

    def test_each_category_has_queries(self):
        """3.3: Each category has at least one query."""
        categories_found = set()
        for query_info in QUERIES.values():
            categories_found.add(query_info['category'])

        expected_categories = {"Competitors", "Trends", "Regional", "Technology"}
        assert categories_found == expected_categories, \
            f"Missing categories: {expected_categories - categories_found}"

    def test_total_query_count(self):
        """Verify we have 18 queries as expected."""
        assert len(QUERIES) == 18, f"Expected 18 queries, found {len(QUERIES)}"


class TestQueryListFiltering:
    """Test query list with filtering (Task 4)."""

    def test_render_query_list_exists(self):
        """4.1: render_query_list function should exist."""
        assert callable(render_query_list)

    def test_filter_queries_by_category_competitors(self):
        """4.3: Filtering by 'Competitors' returns only competitor queries."""
        competitor_queries = [
            qid for qid, qinfo in QUERIES.items()
            if qinfo.get('category') == 'Competitors'
        ]
        # Q06, Q10, Q11, Q12 should be Competitors
        assert len(competitor_queries) >= 4
        assert 'Q06' in competitor_queries
        assert 'Q11' in competitor_queries

    def test_filter_queries_by_category_regional(self):
        """4.3: Filtering by 'Regional' returns regional queries."""
        regional_queries = [
            qid for qid, qinfo in QUERIES.items()
            if qinfo.get('category') == 'Regional'
        ]
        # Q02, Q15, Q16, Q17 should be Regional
        assert len(regional_queries) >= 4
        assert 'Q15' in regional_queries
        assert 'Q17' in regional_queries

    def test_filter_queries_by_category_trends(self):
        """4.3: Filtering by 'Trends' returns trend queries."""
        trend_queries = [
            qid for qid, qinfo in QUERIES.items()
            if qinfo.get('category') == 'Trends'
        ]
        # Q01, Q03, Q07, Q13, Q18 should be Trends
        assert len(trend_queries) >= 4
        assert 'Q03' in trend_queries
        assert 'Q07' in trend_queries

    def test_filter_queries_by_category_technology(self):
        """4.3: Filtering by 'Technology' returns technology queries."""
        tech_queries = [
            qid for qid, qinfo in QUERIES.items()
            if qinfo.get('category') == 'Technology'
        ]
        # Q04, Q05, Q08, Q09, Q14 should be Technology
        assert len(tech_queries) >= 4
        assert 'Q04' in tech_queries
        assert 'Q08' in tech_queries


class TestDetailPage:
    """Test detail page wrapper (Task 5)."""

    def test_render_detail_page_exists(self):
        """5.1: render_detail_page function should exist."""
        assert callable(render_detail_page)

    def test_render_detail_page_shows_back_button(self):
        """5.2: Detail page shows 'Back to Questions' button."""
        # Reset mocks
        mock_st.button = MagicMock(return_value=False)
        mock_st.header = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.divider = MagicMock()
        mock_st.write = MagicMock()
        # Return 4 columns for parameter block
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()])
        mock_st.expander = MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock()))
        mock_container = MagicMock()
        mock_container.__enter__ = MagicMock(return_value=mock_container)
        mock_container.__exit__ = MagicMock(return_value=None)
        mock_st.container = MagicMock(return_value=mock_container)
        mock_st.slider = MagicMock(return_value=(2015, 2024))
        mock_st.multiselect = MagicMock(return_value=["EP", "US", "CN"])
        mock_st.selectbox = MagicMock(return_value=None)
        mock_st.code = MagicMock()
        mock_st.caption = MagicMock()
        mock_st.spinner = MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock()))

        render_detail_page('Q01')

        # Check that a back button was rendered
        back_button_calls = [
            call for call in mock_st.button.call_args_list
            if 'Back' in str(call) or 'back' in str(call).lower()
        ]
        assert len(back_button_calls) >= 1, "Back button should be rendered"


class TestMainRouting:
    """Test main() routing logic (Task 6)."""

    def test_main_calls_init_session_state(self):
        """6.1: main() initializes session state."""
        # Import main
        from app import main

        # Reset session state
        mock_st.session_state.clear()

        # Mock all UI components
        mock_st.stop = MagicMock()
        mock_st.header = MagicMock()
        mock_st.pills = MagicMock(return_value=None)
        mock_st.subheader = MagicMock()
        mock_st.divider = MagicMock()
        mock_st.info = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_col = MagicMock()
        mock_col.__enter__ = MagicMock(return_value=mock_col)
        mock_col.__exit__ = MagicMock(return_value=None)
        mock_st.columns = MagicMock(return_value=[mock_col] * 5)

        # Run main
        main()

        # Session state should be initialized
        assert 'current_page' in mock_st.session_state

    def test_main_routes_to_landing_by_default(self):
        """6.2: main() routes to landing page when current_page == 'landing'."""
        from app import main

        # Reset and set to landing page
        mock_st.session_state.clear()
        mock_st.session_state['current_page'] = 'landing'

        # Mock UI components
        mock_st.stop = MagicMock()
        mock_st.header = MagicMock()
        mock_st.pills = MagicMock(return_value=None)
        mock_st.subheader = MagicMock()
        mock_st.divider = MagicMock()
        mock_st.info = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_col = MagicMock()
        mock_col.__enter__ = MagicMock(return_value=mock_col)
        mock_col.__exit__ = MagicMock(return_value=None)
        mock_st.columns = MagicMock(return_value=[mock_col] * 5)

        main()

        # Should have called header with landing page title
        header_calls = [str(call) for call in mock_st.header.call_args_list]
        assert any('What do you want to know?' in call for call in header_calls)

    def test_main_routes_to_detail_page(self):
        """6.3: main() routes to detail page when current_page == 'detail'."""
        from app import main

        # Reset and set to detail page
        mock_st.session_state.clear()
        mock_st.session_state['current_page'] = 'detail'
        mock_st.session_state['selected_query'] = 'Q01'

        # Mock UI components
        mock_st.stop = MagicMock()
        mock_st.header = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.divider = MagicMock()
        mock_st.write = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        # Return 4 columns for parameter block
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()])
        mock_st.expander = MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock()))
        mock_container = MagicMock()
        mock_container.__enter__ = MagicMock(return_value=mock_container)
        mock_container.__exit__ = MagicMock(return_value=None)
        mock_st.container = MagicMock(return_value=mock_container)
        mock_st.slider = MagicMock(return_value=(2015, 2024))
        mock_st.multiselect = MagicMock(return_value=["EP", "US", "CN"])
        mock_st.selectbox = MagicMock(return_value=None)
        mock_st.code = MagicMock()
        mock_st.caption = MagicMock()

        main()

        # Should have called button with back text
        button_calls = [str(call) for call in mock_st.button.call_args_list]
        assert any('Back' in call for call in button_calls)


# =============================================================================
# Story 1.2: Parameter Block Tests
# =============================================================================

class TestParameterSessionState:
    """Test parameter session state management (Story 1.2 Task 1)."""

    def test_init_session_state_sets_year_range_defaults(self):
        """1.1: year_start and year_end default to sensible values."""
        init_session_state()

        assert mock_st.session_state['year_start'] == 2015
        assert mock_st.session_state['year_end'] == 2024

    def test_init_session_state_sets_jurisdictions_default(self):
        """1.1: jurisdictions defaults to EP, US, CN."""
        init_session_state()

        assert mock_st.session_state['jurisdictions'] == ["EP", "US", "CN"]

    def test_init_session_state_sets_tech_field_default(self):
        """1.1: tech_field defaults to None (all fields)."""
        init_session_state()

        assert mock_st.session_state['tech_field'] is None

    def test_go_to_landing_clears_parameter_state(self):
        """1.3: go_to_landing() clears parameter state (AC #2)."""
        # Set some parameter values
        mock_st.session_state['year_start'] = 2010
        mock_st.session_state['year_end'] = 2020
        mock_st.session_state['jurisdictions'] = ["JP", "KR"]
        mock_st.session_state['tech_field'] = 13

        go_to_landing()

        # Parameters should be reset to defaults
        assert mock_st.session_state['year_start'] == 2015
        assert mock_st.session_state['year_end'] == 2024
        assert mock_st.session_state['jurisdictions'] == ["EP", "US", "CN"]
        assert mock_st.session_state['tech_field'] is None


class TestParameterBlock:
    """Test parameter block component (Story 1.2 Task 3)."""

    def test_render_parameter_block_exists(self):
        """3.1: render_parameter_block function should exist."""
        from app import render_parameter_block
        assert callable(render_parameter_block)

    def test_parameter_block_uses_bordered_container(self):
        """3.2: Parameter block uses st.container(border=True)."""
        from app import render_parameter_block

        # Reset mocks
        mock_container = MagicMock()
        mock_container.__enter__ = MagicMock(return_value=mock_container)
        mock_container.__exit__ = MagicMock(return_value=None)
        mock_st.container = MagicMock(return_value=mock_container)
        mock_st.slider = MagicMock(return_value=(2015, 2024))
        mock_st.multiselect = MagicMock(return_value=["EP", "US", "CN"])
        mock_st.selectbox = MagicMock(return_value=None)
        mock_st.button = MagicMock(return_value=False)
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()])

        render_parameter_block()

        # Check container was called with border=True
        mock_st.container.assert_called_with(border=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
