import { Route, Routes } from "react-router-dom"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Reporte from "./pages/Reporte"

function App() {
  
  return (
    <>
    <div className="bg-primary h-screen" >
      <Routes>
        <Route 
        path="/"
        element={<Home/>}
        />
        <Route
        path="/login"
        element={<Login/>}
        />
        <Route
        path="/reporte"
        element={<Reporte/>}
        />
      </Routes>
    </div>
    </>
  )
}

export default App
