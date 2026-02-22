import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from salesReporter import SalesReporter

class TestSalesReporter:
    @pytest.fixture
    def reporter(self):
        r = SalesReporter()
        r.seed_data()
        yield r
        r.close()

    def test_revenue_by_region_excludes_cancelled(self, reporter):
        results = reporter.revenue_by_region()
        south = next(r for r in results if r['region'] == 'South')
        assert south['total_revenue'] == 75.00, "Should exclude cancelled orders"

    def test_revenue_by_region_correct_north(self, reporter):
        results = reporter.revenue_by_region()
        north = next(r for r in results if r['region'] == 'North')
        assert north['total_revenue'] == 650.00

    def test_customer_report_not_cartesian(self, reporter):
        results = reporter.customer_order_report()
        alice = next(r for r in results if r['name'] == 'Alice')
        assert alice['order_count'] == 2, "Alice has 2 orders, not a cartesian product"

    def test_monthly_revenue_groups_by_month(self, reporter):
        results = reporter.monthly_revenue()
        months = [r['month'] for r in results]
        assert '2026-01' in months, "Should have January (using %m not %M)"
        assert '2026-02' in months, "Should have February"
