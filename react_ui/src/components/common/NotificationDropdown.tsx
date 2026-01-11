import React, { useRef, useEffect } from 'react';
import { Bell, X, CheckCircle2, AlertTriangle, Info, AlertCircle, Trash2 } from 'lucide-react';
import { useNotificationStore, type Notification } from '../../stores/notificationStore';

interface NotificationDropdownProps {
  isOpen: boolean;
  onClose: () => void;
}

const getNotificationIcon = (type: Notification['type']) => {
  switch (type) {
    case 'success':
      return <CheckCircle2 className="w-4 h-4 text-status-success" />;
    case 'error':
      return <AlertCircle className="w-4 h-4 text-status-error" />;
    case 'warning':
      return <AlertTriangle className="w-4 h-4 text-status-warning" />;
    default:
      return <Info className="w-4 h-4 text-primary" />;
  }
};

const getNotificationBgColor = (type: Notification['type']) => {
  switch (type) {
    case 'success':
      return 'bg-status-success/10 border-status-success/20';
    case 'error':
      return 'bg-status-error/10 border-status-error/20';
    case 'warning':
      return 'bg-status-warning/10 border-status-warning/20';
    default:
      return 'bg-primary/10 border-primary/20';
  }
};

const formatTimestamp = (date: Date): string => {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return date.toLocaleDateString();
};

export const NotificationDropdown: React.FC<NotificationDropdownProps> = ({ isOpen, onClose }) => {
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { notifications, markAsRead, markAllAsRead, removeNotification, clearAll, getUnreadCount } = useNotificationStore();
  const unreadCount = getUnreadCount();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={dropdownRef}
      className="absolute top-full right-0 mt-2 w-96 bg-surface border border-secondary-dark rounded-lg shadow-xl z-[100] max-h-[600px] flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-secondary-dark">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-slate-50">Notifications</h3>
          {unreadCount > 0 && (
            <span className="px-2 py-0.5 text-xs font-bold bg-primary text-slate-900 rounded-full">
              {unreadCount}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {unreadCount > 0 && (
            <button
              onClick={markAllAsRead}
              className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-surface-light rounded transition-colors"
              title="Mark all as read"
            >
              <CheckCircle2 className="w-4 h-4" />
            </button>
          )}
          {notifications.length > 0 && (
            <button
              onClick={clearAll}
              className="p-1.5 text-slate-400 hover:text-status-error hover:bg-surface-light rounded transition-colors"
              title="Clear all"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-surface-light rounded transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Notifications List */}
      <div className="overflow-y-auto flex-1">
        {notifications.length === 0 ? (
          <div className="p-8 text-center">
            <Bell className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400 text-sm">No notifications</p>
          </div>
        ) : (
          <div className="divide-y divide-secondary-dark">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`
                  p-4 hover:bg-surface-light transition-colors cursor-pointer
                  ${!notification.read ? 'bg-primary/5' : ''}
                  ${getNotificationBgColor(notification.type)}
                  border-l-4
                  ${notification.type === 'success' ? 'border-status-success' : ''}
                  ${notification.type === 'error' ? 'border-status-error' : ''}
                  ${notification.type === 'warning' ? 'border-status-warning' : ''}
                  ${notification.type === 'info' ? 'border-primary' : ''}
                `}
                onClick={() => {
                  if (!notification.read) {
                    markAsRead(notification.id);
                  }
                  if (notification.action) {
                    notification.action.onClick();
                    onClose();
                  }
                }}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-0.5">
                    {getNotificationIcon(notification.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-sm font-semibold text-slate-50">
                        {notification.title}
                      </h4>
                      {!notification.read && (
                        <div className="w-2 h-2 bg-primary rounded-full flex-shrink-0 mt-1.5" />
                      )}
                    </div>
                    <p className="text-sm text-slate-300 mt-1">
                      {notification.message}
                    </p>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs text-slate-500">
                        {formatTimestamp(notification.timestamp)}
                      </span>
                      {notification.action && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            notification.action?.onClick();
                            onClose();
                          }}
                          className="text-xs text-primary hover:text-primary/80 font-medium"
                        >
                          {notification.action.label}
                        </button>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeNotification(notification.id);
                    }}
                    className="flex-shrink-0 p-1 text-slate-500 hover:text-slate-300 hover:bg-surface rounded transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
