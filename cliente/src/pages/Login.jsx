import { useNavigate } from "react-router-dom";
function Login() {
    const navigate = useNavigate();
    const handleIngresar = () =>{
        navigate("/reporte")
    };


    return (
        <div className="flex flex-col gap-4 justify-center items-center h-screen">
            <div>
                <h1 className="text-white font-bold">Login</h1>
            </div>
            <div className="flex flex-col gap-3 rounded-md p-4 bg-gray-500 ">
                <input type="text" placeholder="Partition" className="px-2 rounded-sm" />
                <input type="text" placeholder="Usuario" className="px-2 rounded-sm" />
                <input type="password" placeholder="Password" className="px-2 rounded-sm" />
                <button className="bg-warning px-8 border-2 rounded-md hover:border-third"
                    onClick={handleIngresar}
                >Ingresar</button>
            </div>
        </div>
    )
}
export default Login;