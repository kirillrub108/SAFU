import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Timetable from './pages/Timetable'
import TimetableGroup from './pages/TimetableGroup'
import TimetableLecturer from './pages/TimetableLecturer'
import GroupsList from './pages/GroupsList'
import AdminHistory from './pages/AdminHistory'
import Import from './pages/Import'
import Subscriptions from './pages/Subscriptions'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/timetable" element={<Timetable />} />
        <Route path="/timetable/group/:id" element={<TimetableGroup />} />
        <Route path="/timetable/lecturer/:id" element={<TimetableLecturer />} />
        <Route path="/groups" element={<GroupsList />} />
        <Route path="/admin/history" element={<AdminHistory />} />
        <Route path="/admin/import" element={<Import />} />
        <Route path="/calendar/subscriptions" element={<Subscriptions />} />
      </Routes>
    </Layout>
  )
}

export default App

