/**
 * Dashboard page
 */
import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useAuthStore } from '../store/authStore';
import { useAnalyticsStore } from '../store/analyticsStore';
import { analyticsService } from '../services/analytics';

export default function Dashboard() {
  const { user } = useAuthStore();
  const { dashboardData, setDashboardData, setLoading } = useAnalyticsStore();

  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true);
      try {
        const data = await analyticsService.getDashboard();
        setDashboardData(data);
      } catch (error) {
        console.error('Failed to load dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [setDashboardData, setLoading]);

  if (!dashboardData) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-primary text-white p-6">
        <h1 className="text-3xl font-bold">Welcome, {user?.full_name || user?.email}! 👋</h1>
        <p className="text-gray-200">Track your carbon footprint and reduce your impact</p>
      </div>

      {/* Stats Grid */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Today', value: dashboardData.today_emissions.toFixed(2), unit: 'kg CO₂' },
            { label: 'This Month', value: dashboardData.this_month_emissions.toFixed(2), unit: 'kg CO₂' },
            { label: 'This Year', value: dashboardData.this_year_emissions.toFixed(2), unit: 'kg CO₂' },
            { label: 'Total', value: dashboardData.total_emissions.toFixed(2), unit: 'kg CO₂' },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-secondary"
            >
              <p className="text-gray-600 text-sm font-semibold">{stat.label}</p>
              <p className="text-3xl font-bold text-primary mt-2">
                {stat.value} <span className="text-sm text-gray-600">{stat.unit}</span>
              </p>
            </motion.div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Sample Chart 1 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h2 className="text-xl font-bold text-primary mb-4">Weekly Emissions</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[
                { day: 'Mon', emissions: 2.5 },
                { day: 'Tue', emissions: 3.2 },
                { day: 'Wed', emissions: 2.1 },
                { day: 'Thu', emissions: 3.5 },
                { day: 'Fri', emissions: 4.2 },
                { day: 'Sat', emissions: 1.8 },
                { day: 'Sun', emissions: 2.0 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="emissions" fill="#2BAE66" />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Sample Chart 2 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h2 className="text-xl font-bold text-primary mb-4">Monthly Trend</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={[
                { week: 'W1', emissions: 15 },
                { week: 'W2', emissions: 18 },
                { week: 'W3', emissions: 16 },
                { week: 'W4', emissions: 14 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="emissions" stroke="#0F6D3B" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Activity Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="bg-white rounded-xl shadow-lg p-6 mt-8"
        >
          <h2 className="text-xl font-bold text-primary mb-4">Activity Overview</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Activities', value: dashboardData.activities_count },
              { label: 'Active Goals', value: dashboardData.active_goals },
              { label: 'Points', value: dashboardData.total_points },
              { label: 'Achievements', value: 0 },
            ].map((item, index) => (
              <div key={index} className="text-center p-4 bg-background rounded-lg">
                <p className="text-gray-600 text-sm">{item.label}</p>
                <p className="text-2xl font-bold text-primary">{item.value}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
