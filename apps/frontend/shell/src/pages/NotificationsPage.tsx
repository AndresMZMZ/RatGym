import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  read: boolean;
  created_at: string;
  metadata?: any;
}

interface NotificationStats {
  total: number;
  unread: number;
  read: number;
  by_type: { [key: string]: number };
  by_priority: { [key: string]: number };
}

export const NotificationsPage: React.FC = () => {
  const navigate = useNavigate();
  const currentUser = localStorage.getItem('ratgym_username') || 'juan';
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [stats, setStats] = useState<NotificationStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'unread' | 'read'>('all');

  useEffect(() => {
    fetchNotifications();
    fetchStats();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await fetch(`http://localhost:3006/notifications/user/${currentUser}`);
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`http://localhost:3006/notifications/user/${currentUser}/stats`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const markAsRead = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:3006/notifications/${id}/read`, {
        method: 'PATCH',
      });
      if (response.ok) {
        setNotifications(notifications.map(n => 
          n.id === id ? { ...n, read: true } : n
        ));
        fetchStats();
      }
    } catch (error) {
      console.error('Error marking as read:', error);
    }
  };

  const deleteNotification = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:3006/notifications/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        setNotifications(notifications.filter(n => n.id !== id));
        fetchStats();
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH': return '#ef4444';
      case 'MEDIUM': return '#f59e0b';
      case 'LOW': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getTypeIcon = (type: string) => {
    const icons: { [key: string]: string } = {
      'ROUTINE_ASSIGNED': '💪',
      'DAILY_ROUTINE': '📅',
      'ROUTINE_COMPLETED': '✅',
      'REST_DAY': '😴',
      'NUTRITION_PLAN': '🥗',
      'MEAL_REMINDER': '🍽️',
      'GOAL_ACHIEVED': '🏆',
      'CLASS_SCHEDULED': '🎯',
      'CLASS_REMINDER': '⏰',
      'CLASS_CANCELLED': '❌',
      'SYSTEM_INFO': '🔔',
    };
    return icons[type] || '📬';
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Hace menos de 1 hora';
    if (hours < 24) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `Hace ${days} día${days > 1 ? 's' : ''}`;
    return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
  };

  const filteredNotifications = notifications.filter(n => {
    if (filter === 'unread') return !n.read;
    if (filter === 'read') return n.read;
    return true;
  });

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#000',
        color: '#fff',
        padding: '32px 40px',
        borderBottom: '1px solid #333',
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <button
            onClick={() => navigate('/')}
            style={{
              background: 'none',
              border: 'none',
              color: '#fff',
              cursor: 'pointer',
              fontSize: '16px',
              marginBottom: '16px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 0',
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '0.7'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '1'}
          >
            ← Volver al Dashboard
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
            <div style={{ fontSize: '40px' }}>🔔</div>
            <div>
              <h1 style={{
                fontSize: '32px',
                fontWeight: '700',
                margin: 0,
                letterSpacing: '-0.5px',
              }}>
                Notificaciones
              </h1>
              <p style={{ fontSize: '16px', color: '#999', margin: '4px 0 0 0' }}>
                Todas tus alertas y recordatorios
              </p>
            </div>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
              gap: '16px',
              marginTop: '24px',
            }}>
              <div style={{
                backgroundColor: '#1a1a1a',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid #333',
              }}>
                <div style={{ fontSize: '24px', fontWeight: '700', marginBottom: '4px' }}>
                  {stats.total}
                </div>
                <div style={{ fontSize: '13px', color: '#999' }}>Total</div>
              </div>
              <div style={{
                backgroundColor: '#1a1a1a',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid #333',
              }}>
                <div style={{ fontSize: '24px', fontWeight: '700', marginBottom: '4px', color: '#3b82f6' }}>
                  {stats.unread}
                </div>
                <div style={{ fontSize: '13px', color: '#999' }}>No leídas</div>
              </div>
              <div style={{
                backgroundColor: '#1a1a1a',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid #333',
              }}>
                <div style={{ fontSize: '24px', fontWeight: '700', marginBottom: '4px', color: '#10b981' }}>
                  {stats.read}
                </div>
                <div style={{ fontSize: '13px', color: '#999' }}>Leídas</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '32px 40px',
      }}>
        {/* Filters */}
        <div style={{
          display: 'flex',
          gap: '12px',
          marginBottom: '24px',
          flexWrap: 'wrap',
        }}>
          {[
            { value: 'all', label: 'Todas' },
            { value: 'unread', label: 'No leídas' },
            { value: 'read', label: 'Leídas' },
          ].map((btn) => (
            <button
              key={btn.value}
              onClick={() => setFilter(btn.value as any)}
              style={{
                padding: '10px 20px',
                fontSize: '14px',
                fontWeight: '600',
                color: filter === btn.value ? '#fff' : '#000',
                backgroundColor: filter === btn.value ? '#000' : '#fff',
                border: '1px solid #e0e0e0',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
              onMouseEnter={(e) => {
                if (filter !== btn.value) {
                  e.currentTarget.style.borderColor = '#000';
                }
              }}
              onMouseLeave={(e) => {
                if (filter !== btn.value) {
                  e.currentTarget.style.borderColor = '#e0e0e0';
                }
              }}
            >
              {btn.label}
            </button>
          ))}
        </div>

        {/* Loading */}
        {loading && (
          <div style={{ textAlign: 'center', padding: '60px 20px', color: '#666' }}>
            <div style={{ fontSize: '40px', marginBottom: '16px' }}>⏳</div>
            <div>Cargando notificaciones...</div>
          </div>
        )}

        {/* Empty State */}
        {!loading && filteredNotifications.length === 0 && (
          <div style={{
            backgroundColor: '#fff',
            padding: '60px 40px',
            borderRadius: '8px',
            border: '1px solid #e0e0e0',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '60px', marginBottom: '16px', opacity: 0.3 }}>🔔</div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#000', marginBottom: '8px' }}>
              No hay notificaciones
            </h3>
            <p style={{ fontSize: '14px', color: '#666' }}>
              {filter === 'unread' && 'No tienes notificaciones sin leer'}
              {filter === 'read' && 'No tienes notificaciones leídas'}
              {filter === 'all' && 'Cuando recibas notificaciones aparecerán aquí'}
            </p>
          </div>
        )}

        {/* Notifications List */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}>
          {filteredNotifications.map((notification) => (
            <div
              key={notification.id}
              style={{
                backgroundColor: '#fff',
                padding: '24px',
                borderRadius: '8px',
                border: `1px solid ${notification.read ? '#e0e0e0' : '#3b82f6'}`,
                borderLeft: `4px solid ${getPriorityColor(notification.priority)}`,
                transition: 'all 0.2s',
                opacity: notification.read ? 0.7 : 1,
              }}
              onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)'}
              onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
            >
              <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
                {/* Icon */}
                <div style={{
                  fontSize: '32px',
                  flexShrink: 0,
                }}>
                  {getTypeIcon(notification.type)}
                </div>

                {/* Content */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px', marginBottom: '8px' }}>
                    <h3 style={{
                      fontSize: '18px',
                      fontWeight: '600',
                      color: '#000',
                      margin: 0,
                      lineHeight: '1.4',
                    }}>
                      {notification.title}
                    </h3>
                    {!notification.read && (
                      <span style={{
                        backgroundColor: '#3b82f6',
                        color: '#fff',
                        fontSize: '11px',
                        fontWeight: '700',
                        padding: '4px 8px',
                        borderRadius: '4px',
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px',
                        flexShrink: 0,
                      }}>
                        Nueva
                      </span>
                    )}
                  </div>
                  <p style={{
                    fontSize: '14px',
                    color: '#666',
                    lineHeight: '1.6',
                    margin: '0 0 12px 0',
                  }}>
                    {notification.message}
                  </p>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    fontSize: '13px',
                    color: '#999',
                  }}>
                    <span>{formatDate(notification.created_at)}</span>
                    <span style={{
                      padding: '4px 10px',
                      backgroundColor: '#f3f4f6',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: '500',
                    }}>
                      {notification.type.replace(/_/g, ' ')}
                    </span>
                    <span style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      backgroundColor: getPriorityColor(notification.priority),
                    }} />
                  </div>

                  {/* Actions */}
                  <div style={{
                    display: 'flex',
                    gap: '12px',
                    marginTop: '16px',
                    paddingTop: '16px',
                    borderTop: '1px solid #f0f0f0',
                  }}>
                    {!notification.read && (
                      <button
                        onClick={() => markAsRead(notification.id)}
                        style={{
                          padding: '8px 16px',
                          fontSize: '13px',
                          fontWeight: '600',
                          color: '#3b82f6',
                          backgroundColor: 'transparent',
                          border: '1px solid #3b82f6',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          transition: 'all 0.2s',
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.backgroundColor = '#3b82f6';
                          e.currentTarget.style.color = '#fff';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.backgroundColor = 'transparent';
                          e.currentTarget.style.color = '#3b82f6';
                        }}
                      >
                        ✓ Marcar como leída
                      </button>
                    )}
                    <button
                      onClick={() => deleteNotification(notification.id)}
                      style={{
                        padding: '8px 16px',
                        fontSize: '13px',
                        fontWeight: '600',
                        color: '#ef4444',
                        backgroundColor: 'transparent',
                        border: '1px solid #ef4444',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = '#ef4444';
                        e.currentTarget.style.color = '#fff';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = 'transparent';
                        e.currentTarget.style.color = '#ef4444';
                      }}
                    >
                      🗑️ Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
