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
}

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>('');
  const [currentUser, setCurrentUser] = useState<string | null>(
    localStorage.getItem('ratgym_username')
  );
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (currentUser) {
      fetchNotifications();
    }
  }, [currentUser]);

  const fetchNotifications = async () => {
    try {
      const response = await fetch(`http://localhost:3006/notifications/user/${currentUser}`);
      if (response.ok) {
        const data = await response.json();
        // Ordenar por fecha (más recientes primero) y tomar solo las últimas 4
        const sortedNotifications = data
          .sort((a: Notification, b: Notification) => 
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          )
          .slice(0, 4);
        setNotifications(sortedNotifications);
        setUnreadCount(data.filter((n: Notification) => !n.read).length);
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
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

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Hace menos de 1h';
    if (hours < 24) return `Hace ${hours}h`;
    const days = Math.floor(hours / 24);
    return `Hace ${days}d`;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (username.trim()) {
      localStorage.setItem('ratgym_username', username.trim());
      setCurrentUser(username.trim());
      setUsername('');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('ratgym_username');
    setCurrentUser(null);
  };

  // Pantalla de login
  if (!currentUser) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#000',
      }}>
        <div style={{
          maxWidth: '450px',
          width: '100%',
          padding: '50px 40px',
          backgroundColor: '#fff',
          borderRadius: '8px',
          boxShadow: '0 10px 40px rgba(0,0,0,0.3)',
        }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <div style={{
              width: '80px',
              height: '80px',
              backgroundColor: '#000',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '40px',
              margin: '0 auto 20px',
            }}>
              🐀
            </div>
            <h1 style={{
              fontSize: '32px',
              fontWeight: '700',
              color: '#000',
              marginBottom: '10px',
              letterSpacing: '-0.5px',
            }}>
              RATGYM
            </h1>
            <p style={{
              fontSize: '14px',
              color: '#666',
            }}>
              Ingresa tu nombre para continuar
            </p>
          </div>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Nombre de usuario"
              required
              autoFocus
              style={{
                width: '100%',
                padding: '16px',
                fontSize: '15px',
                border: '2px solid #e0e0e0',
                borderRadius: '4px',
                marginBottom: '20px',
                outline: 'none',
                transition: 'border-color 0.2s',
                fontWeight: '500',
              }}
              onFocus={(e) => e.target.style.borderColor = '#000'}
              onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
            />
            <button
              type="submit"
              style={{
                width: '100%',
                padding: '16px',
                fontSize: '16px',
                fontWeight: '700',
                color: '#fff',
                backgroundColor: '#000',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#333'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#000'}
            >
              Ingresar
            </button>
          </form>
        </div>
      </div>
    );
  }

  // Dashboard principal
  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Sidebar */}
      <div style={{
        width: sidebarOpen ? '280px' : '80px',
        backgroundColor: '#000',
        color: '#fff',
        transition: 'width 0.3s ease',
        position: 'fixed',
        height: '100vh',
        overflowY: 'auto',
        zIndex: 1000,
      }}>
        {/* Header del Sidebar */}
        <div style={{
          padding: '24px 20px',
          borderBottom: '1px solid #333',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          {sidebarOpen ? (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  backgroundColor: '#fff',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '20px',
                }}>
                  🐀
                </div>
                <span style={{ fontSize: '20px', fontWeight: '700', letterSpacing: '1px' }}>RATGYM</span>
              </div>
              <button
                onClick={() => setSidebarOpen(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#fff',
                  cursor: 'pointer',
                  fontSize: '20px',
                }}
              >
                ←
              </button>
            </>
          ) : (
            <button
              onClick={() => setSidebarOpen(true)}
              style={{
                background: 'none',
                border: 'none',
                color: '#fff',
                cursor: 'pointer',
                fontSize: '24px',
                margin: '0 auto',
              }}
            >
              →
            </button>
          )}
        </div>

        {/* Usuario */}
        <div style={{
          padding: '20px',
          borderBottom: '1px solid #333',
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
          }}>
            <div style={{
              width: '50px',
              height: '50px',
              backgroundColor: '#333',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px',
              flexShrink: 0,
            }}>
              👤
            </div>
            {sidebarOpen && (
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontWeight: '600',
                  fontSize: '16px',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}>
                  {currentUser}
                </div>
                <div style={{
                  fontSize: '12px',
                  color: '#999',
                  marginTop: '2px',
                }}>
                  Usuario activo
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Menú */}
        <nav style={{ padding: '20px 0' }}>
          {menuItems.map((item, index) => (
            <div
              key={index}
              style={{
                padding: sidebarOpen ? '14px 20px' : '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '16px',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
                backgroundColor: index === 0 ? '#1a1a1a' : 'transparent',
                borderLeft: index === 0 ? '4px solid #fff' : '4px solid transparent',
              }}
              onMouseEnter={(e) => {
                if (index !== 0) e.currentTarget.style.backgroundColor = '#1a1a1a';
              }}
              onMouseLeave={(e) => {
                if (index !== 0) e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              <span style={{ fontSize: '20px', flexShrink: 0 }}>{item.icon}</span>
              {sidebarOpen && (
                <span style={{ fontSize: '15px', fontWeight: '500' }}>{item.label}</span>
              )}
            </div>
          ))}
        </nav>

        {/* Botón de cerrar sesión */}
        {sidebarOpen && (
          <div style={{ padding: '20px', position: 'absolute', bottom: 0, width: '100%' }}>
            <button
              onClick={handleLogout}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '14px',
                fontWeight: '600',
                color: '#fff',
                backgroundColor: '#333',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#444'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#333'}
            >
              Cambiar Usuario
            </button>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div style={{
        flex: 1,
        marginLeft: sidebarOpen ? '280px' : '80px',
        transition: 'margin-left 0.3s ease',
        padding: '40px',
      }}>
        {/* Header */}
        <div style={{ marginBottom: '40px' }}>
          <h1 style={{
            fontSize: '32px',
            fontWeight: '700',
            color: '#000',
            marginBottom: '8px',
            letterSpacing: '-0.5px',
          }}>
            Dashboard
          </h1>
          <p style={{ fontSize: '16px', color: '#666' }}>
            Bienvenido de nuevo, {currentUser}
          </p>
        </div>

        {/* Stats Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '20px',
          marginBottom: '40px',
        }}>
          {statsCards.map((card, index) => (
            <div
              key={index}
              style={{
                backgroundColor: '#fff',
                padding: '24px',
                borderRadius: '8px',
                border: '1px solid #e0e0e0',
                transition: 'box-shadow 0.2s',
                cursor: 'pointer',
              }}
              onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)'}
              onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
            >
              <div style={{ fontSize: '32px', marginBottom: '12px' }}>{card.icon}</div>
              <div style={{ fontSize: '28px', fontWeight: '700', color: '#000', marginBottom: '4px' }}>
                {card.value}
              </div>
              <div style={{ fontSize: '14px', color: '#666', fontWeight: '500' }}>
                {card.label}
              </div>
            </div>
          ))}
        </div>

        {/* Widgets Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
          gap: '24px',
        }}>
          {widgets.map((widget, index) => (
            <div
              key={index}
              style={{
                backgroundColor: '#fff',
                borderRadius: '8px',
                border: '1px solid #e0e0e0',
                overflow: 'hidden',
                transition: 'box-shadow 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)'}
              onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
            >
              {/* Widget Header */}
              <div style={{
                padding: '20px 24px',
                borderBottom: '1px solid #f0f0f0',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
              }}>
                <div style={{ fontSize: '24px' }}>{widget.icon}</div>
                <div style={{ flex: 1 }}>
                  <h3 style={{
                    fontSize: '18px',
                    fontWeight: '600',
                    color: '#000',
                    marginBottom: '2px',
                  }}>
                    {widget.title}
                  </h3>
                  <p style={{ fontSize: '13px', color: '#999', margin: 0 }}>
                    {widget.subtitle}
                  </p>
                </div>
                {widget.title === 'Notificaciones' && unreadCount > 0 && (
                  <div style={{
                    backgroundColor: '#ef4444',
                    color: '#fff',
                    fontSize: '12px',
                    fontWeight: '700',
                    padding: '4px 10px',
                    borderRadius: '12px',
                    minWidth: '24px',
                    textAlign: 'center',
                  }}>
                    {unreadCount}
                  </div>
                )}
              </div>

              {/* Widget Content */}
              <div style={{
                padding: widget.title === 'Notificaciones' && notifications.length > 0 ? '0' : '24px',
                minHeight: '120px',
                display: 'flex',
                alignItems: widget.title === 'Notificaciones' && notifications.length > 0 ? 'stretch' : 'center',
                justifyContent: 'center',
                backgroundColor: '#fafafa',
              }}>
                {widget.title === 'Notificaciones' && notifications.length > 0 ? (
                  <div style={{ width: '100%' }}>
                    {notifications.map((notification, nIndex) => (
                      <div
                        key={notification.id}
                        style={{
                          padding: '16px 24px',
                          borderBottom: nIndex < notifications.length - 1 ? '1px solid #f0f0f0' : 'none',
                          display: 'flex',
                          gap: '12px',
                          alignItems: 'flex-start',
                          backgroundColor: notification.read ? '#fafafa' : '#fff',
                          cursor: 'pointer',
                          transition: 'background-color 0.2s',
                        }}
                        onClick={() => navigate('/notifications')}
                        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f3f4f6'}
                        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = notification.read ? '#fafafa' : '#fff'}
                      >
                        <div style={{ fontSize: '20px', flexShrink: 0 }}>
                          {getTypeIcon(notification.type)}
                        </div>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', marginBottom: '4px' }}>
                            <div style={{
                              fontSize: '14px',
                              fontWeight: '600',
                              color: '#000',
                              lineHeight: '1.4',
                              flex: 1,
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                            }}>
                              {notification.title}
                            </div>
                            {!notification.read && (
                              <div style={{
                                width: '8px',
                                height: '8px',
                                backgroundColor: '#3b82f6',
                                borderRadius: '50%',
                                flexShrink: 0,
                                marginTop: '4px',
                              }} />
                            )}
                          </div>
                          <p style={{
                            fontSize: '13px',
                            color: '#666',
                            lineHeight: '1.4',
                            margin: '0 0 6px 0',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}>
                            {notification.message}
                          </p>
                          <span style={{
                            fontSize: '12px',
                            color: '#999',
                          }}>
                            {formatTimeAgo(notification.created_at)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : widget.title === 'Notificaciones' ? (
                  <div style={{
                    textAlign: 'center',
                    color: '#999',
                    fontSize: '14px',
                    padding: '24px',
                  }}>
                    <div style={{ fontSize: '40px', marginBottom: '12px', opacity: 0.3 }}>
                      {widget.icon}
                    </div>
                    <div>No hay notificaciones</div>
                  </div>
                ) : (
                  <div style={{
                    textAlign: 'center',
                    color: '#999',
                    fontSize: '14px',
                  }}>
                    <div style={{ fontSize: '40px', marginBottom: '12px', opacity: 0.3 }}>
                      {widget.icon}
                    </div>
                    <div>Esperando integración de microservicio</div>
                  </div>
                )}
              </div>

              {/* Widget Footer */}
              <div style={{
                padding: '16px 24px',
                backgroundColor: '#f8f9fa',
                borderTop: '1px solid #f0f0f0',
              }}>
                <button
                  onClick={() => {
                    // Si es el widget de Notificaciones (índice 4), navegar a la página de notificaciones
                    if (widget.title === 'Notificaciones') {
                      navigate('/notifications');
                    }
                  }}
                  style={{
                    width: '100%',
                    padding: '10px',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: '#000',
                    backgroundColor: 'transparent',
                    border: '1px solid #e0e0e0',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#000';
                    e.currentTarget.style.color = '#fff';
                    e.currentTarget.style.borderColor = '#000';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.color = '#000';
                    e.currentTarget.style.borderColor = '#e0e0e0';
                  }}
                >
                  Ver más →
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Datos del menú
const menuItems = [
  { icon: '🏠', label: 'Dashboard' },
  { icon: '💪', label: 'Mis Rutinas' },
  { icon: '🎯', label: 'Clases' },
  { icon: '🥗', label: 'Nutrición' },
  { icon: '📊', label: 'Progreso' },
  { icon: '🔔', label: 'Notificaciones' },
  { icon: '⚙️', label: 'Configuración' },
];

// Tarjetas de estadísticas
const statsCards = [
  { icon: '🔥', value: '0', label: 'Entrenamientos' },
  { icon: '⏱️', value: '0h', label: 'Tiempo Total' },
  { icon: '🎯', value: '0', label: 'Objetivos' },
  { icon: '📈', value: '0%', label: 'Progreso' },
];

// Widgets
const widgets = [
  { icon: '💪', title: 'Rutinas', subtitle: 'Tus entrenamientos personalizados' },
  { icon: '🎯', title: 'Clases', subtitle: 'Próximas sesiones grupales' },
  { icon: '🥗', title: 'Nutrición', subtitle: 'Plan alimenticio' },
  { icon: '📊', title: 'Estadísticas', subtitle: 'Tu rendimiento' },
  { icon: '🔔', title: 'Notificaciones', subtitle: 'Alertas y recordatorios' },
  { icon: '✨', title: 'Recomendaciones', subtitle: 'Sugerencias para ti' },
];
