import { Route, Routes } from "react-router-dom"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Reporte from "./pages/Reporte"
import Tarjeta from "./pages/Tarjeta"

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
        <Route
        path="/tarjeta"
        element={<Tarjeta/>}
        />
      </Routes>
    </div>
    </>
  )
}

export default App
