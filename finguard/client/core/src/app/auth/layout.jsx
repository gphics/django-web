import { ToastContainer } from "react-toastify"

function layout({children}) {
  return (
      <>
          <ToastContainer theme="dark" position="top-center"/>
          {children}
          
      </>
  )
}

export default layout