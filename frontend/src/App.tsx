import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Timetable from './pages/Timetable'
import TimetableGroup from './pages/TimetableGroup'
import TimetableLecturer from './pages/TimetableLecturer'
import Import from './pages/Import'
import Login from './pages/Login'
import Register from './pages/Register'
import Favorites from './pages/Favorites'
import Notifications from './pages/Notifications'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Timetable />} />
        <Route path="/timetable/group/:id" element={<TimetableGroup />} />
        <Route path="/timetable/lecturer/:id" element={<TimetableLecturer />} />
        <Route path="/admin/import" element={<Import />} />
        <Route path="/auth/login" element={<Login />} />
        <Route path="/auth/register" element={<Register />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/notifications" element={<Notifications />} />
      </Routes>
    </Layout>
  )
}

export default App

