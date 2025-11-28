import { Link } from 'react-router-dom'
import { useState } from 'react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8">
          <div className="flex justify-between items-center py-3 md:py-4">
            <Link to="/" className="text-xl md:text-2xl font-bold text-blue-600">
              САФУ Расписание
            </Link>
            
            {/* Мобильное меню - кнопка */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-md text-gray-700 hover:bg-gray-100"
              aria-label="Меню"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {mobileMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
            
            {/* Десктопное меню */}
            <nav className="hidden md:flex space-x-4">
              <Link to="/" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                Главная
              </Link>
              <Link to="/groups" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                Группы
              </Link>
              <Link to="/timetable" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                Расписание
              </Link>
              <Link to="/admin/history" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                История
              </Link>
              <Link to="/admin/import" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                Импорт
              </Link>
              <Link to="/calendar/subscriptions" className="text-gray-700 hover:text-blue-600 px-2 py-1">
                Подписки
              </Link>
            </nav>
          </div>
          
          {/* Мобильное меню - выпадающий список */}
          {mobileMenuOpen && (
            <nav className="md:hidden pb-4 border-t border-gray-200 mt-2 pt-4">
              <div className="flex flex-col space-y-2">
                <Link
                  to="/"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  Главная
                </Link>
                <Link
                  to="/groups"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  Группы
                </Link>
                <Link
                  to="/timetable"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  Расписание
                </Link>
                <Link
                  to="/admin/history"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  История
                </Link>
                <Link
                  to="/admin/import"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  Импорт
                </Link>
                <Link
                  to="/calendar/subscriptions"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                >
                  Подписки
                </Link>
              </div>
            </nav>
          )}
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 md:py-8">
        {children}
      </main>
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-gray-600 text-sm">
          <p>© 2025 САФУ Расписание</p>
        </div>
      </footer>
    </div>
  )
}

