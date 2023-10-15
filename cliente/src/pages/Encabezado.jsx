import { useNavigate } from "react-router-dom";

// eslint-disable-next-line react/prop-types
function Encabezado({ Contenido, Ejecutar }) {
    const navigate = useNavigate();
    const handleLogin = () => {
        navigate("/login")
    };

    const handleFileSelected = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = (e) => {
            const text = e.target.result;
            Contenido(text)
        }
    }

    return (
        <div className="flex items-center h-7 gap-5 justify-between p-5">
            <input className="text-2xl  bg-gray-500 border-2 rounded-md hover:border-black" type="File"
                onChange={handleFileSelected}
            ></input>
            <button
                className="text-3xl  bg-warning px-8 border-2 rounded-md hover:border-third"
                onClick={Ejecutar} >
                Ejecutar </button>
            <button className="text-3xl bg-warning px-8 border-2 rounded-md hover:border-third"
                onClick={handleLogin}
            > Iniciar Sesión</button>
        </div>
    )
}

export default Encabezado;