import React, { useState } from 'react';
import { Bell, Search } from 'lucide-react';
import { NotificationDropdown } from '../common/NotificationDropdown';
import { useNotificationStore } from '../../stores/notificationStore';

export const Header: React.FC = () => {
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const { getUnreadCount } = useNotificationStore();
    const unreadCount = getUnreadCount();

    return (
        <header className="h-16 bg-surface border-b border-secondary-dark flex items-center justify-between px-6">
            <div className="flex items-center gap-4 flex-1">
                <div className="relative w-96">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                        type="text"
                        placeholder="Search reports, samples, or CRMs..."
                        className="w-full pl-10 pr-4 py-2 bg-surface-light border-none rounded-lg text-sm text-slate-50 placeholder:text-slate-500 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                    />
                </div>
            </div>

            <div className="flex items-center gap-4">
                <div className="relative z-[60]">
                    <button 
                        onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                        className="p-2 text-slate-400 hover:text-primary transition-colors relative"
                        title="Notifications"
                    >
                        <Bell className="w-5 h-5" />
                        {unreadCount > 0 && (
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-status-error rounded-full border-2 border-surface" />
                        )}
                    </button>
                    <NotificationDropdown 
                        isOpen={isNotificationOpen} 
                        onClose={() => setIsNotificationOpen(false)} 
                    />
                </div>

                <div className="h-8 w-px bg-secondary-dark" />

                <button className="flex items-center gap-3 pl-2">
                    <div className="text-right hidden sm:block">
                        <p className="text-sm font-medium text-slate-50">Geologist</p>
                        <p className="text-xs text-slate-400">Admin Access</p>
                    </div>
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center text-primary font-bold">
                        G
                    </div>
                </button>
            </div>
        </header>
    );
};
