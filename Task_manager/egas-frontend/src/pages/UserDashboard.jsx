import { useEffect, useState } from 'react';
import './UserDashboard.css';

const mockDashboardData = {
  employee: {
    name: 'أحمد علي',
    role: 'مطور Frontend',
    department: 'قسم التطوير',
  },
  attendance: {
    attended: 18,
    absent: 4,
  },
  tasks: {
    completed: 12,
    pending: 6,
    missed: 3,
  },
};

const metricStyles = {
  attended: 'success',
  absent: 'danger',
  completed: 'success',
  pending: 'warning',
  missed: 'danger',
};

const metricConfig = [
  { key: 'attended', label: 'Days Attended', arabicLabel: 'حضر', valueKey: 'attendance.attended', tone: 'success' },
  { key: 'absent', label: 'Days Absent', arabicLabel: 'غاب', valueKey: 'attendance.absent', tone: 'danger' },
  { key: 'completed', label: 'Completed Tasks', arabicLabel: 'منتهية', valueKey: 'tasks.completed', tone: 'success' },
  { key: 'pending', label: 'Pending Tasks', arabicLabel: 'قيد الانتظار', valueKey: 'tasks.pending', tone: 'warning' },
  { key: 'missed', label: 'Missed / Overdue Tasks', arabicLabel: 'فائتة / لم تكتمل', valueKey: 'tasks.missed', tone: 'danger' },
];

function getNestedValue(data, path) {
  return path.split('.').reduce((acc, key) => acc?.[key], data);
}

function UserDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDashboardData(mockDashboardData);
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  if (loading || !dashboardData) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-shell">
          <div className="loading-state">
            <div className="loading-spinner" />
            <p>Loading dashboard data...</p>
          </div>
        </div>
      </div>
    );
  }

  const totalTasks = dashboardData.tasks.completed + dashboardData.tasks.pending + dashboardData.tasks.missed;
  const totalAttendanceDays = dashboardData.attendance.attended + dashboardData.attendance.absent;

  return (
    <div className="dashboard-page">
      <div className="dashboard-shell">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">Employee Overview</p>
            <h1>Welcome back, {dashboardData.employee.name}</h1>
          </div>

          <div className="profile-pill">
            <span className="profile-dot" />
            <div>
              <strong>{dashboardData.employee.role}</strong>
              <small>{dashboardData.employee.department}</small>
            </div>
          </div>
        </header>

        <section className="stats-grid" aria-label="Employee statistics">
          {metricConfig.map((metric) => {
            const value = getNestedValue(dashboardData, metric.valueKey);

            return (
              <article key={metric.key} className={`metric-card ${metric.tone}`}>
                <div className="metric-topline">
                  <span className="metric-label">{metric.label}</span>
                  <span className="metric-arabic">{metric.arabicLabel}</span>
                </div>

                <div className="metric-value-row">
                  <strong className="metric-value">{value}</strong>
                  <span className={`metric-badge ${metric.tone}`}>
                    {metric.key === 'attended' || metric.key === 'completed' ? 'Good' : metric.key === 'pending' ? 'In Progress' : 'Needs Attention'}
                  </span>
                </div>
              </article>
            );
          })}
        </section>

        <section className="summary-panel">
          <div className="summary-card">
            <h2>Attendance Summary</h2>
            <div className="progress-row">
              <span>Attendance rate</span>
              <strong>{Math.round((dashboardData.attendance.attended / totalAttendanceDays) * 100)}%</strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill success"
                style={{ width: `${(dashboardData.attendance.attended / totalAttendanceDays) * 100}%` }}
              />
            </div>

            <ul className="summary-list">
              <li>
                <span>Attended days</span>
                <strong>{dashboardData.attendance.attended}</strong>
              </li>
              <li>
                <span>Absent days</span>
                <strong>{dashboardData.attendance.absent}</strong>
              </li>
            </ul>
          </div>

          <div className="summary-card">
            <h2>Task Summary</h2>
            <div className="progress-row">
              <span>Completion rate</span>
              <strong>{Math.round((dashboardData.tasks.completed / totalTasks) * 100)}%</strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill success"
                style={{ width: `${(dashboardData.tasks.completed / totalTasks) * 100}%` }}
              />
            </div>

            <ul className="summary-list">
              <li>
                <span>Completed</span>
                <strong>{dashboardData.tasks.completed}</strong>
              </li>
              <li>
                <span>Pending</span>
                <strong>{dashboardData.tasks.pending}</strong>
              </li>
              <li>
                <span>Missed</span>
                <strong>{dashboardData.tasks.missed}</strong>
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
}

export default UserDashboard;
