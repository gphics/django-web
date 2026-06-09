"use client"

import sendRequest from "@/utils/requestSender"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { toast, ToastContainer } from "react-toastify"
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"

function TransactionAction({ id }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  
  function updateHandler() {
    router.push("/transaction/create?id="+id)
  }
  async function deleteHandler() {
    setIsLoading(true)
    const url = "transaction/?id=" + id
    const res = await sendRequest(url, { method: "DELETE" })

    setIsLoading(false)
    if (!res?.success || res.err) {
      toast.error(res?.err[0])
      return
    }

    // back to home
    router.replace("/dashboard")
  }
  return (
    <div className="flex justify-around items-center mx-auto w-[300px] my-3">
      {!!isLoading && <FullPageLoadingComponent/>}
      <ToastContainer theme="dark"  position="top-center" />
          <button className="bg-emerald-400 poppins-bold px-5 py-2 cursor-pointer transition-all duration-200 hover:scale-[1.05] hover:text-white rounded-md" type="button" onClick={updateHandler}>Update</button>

          <button className="bg-rose-400 poppins-bold px-5 py-2 cursor-pointer transition-all duration-200 hover:scale-[1.05] hover:text-white rounded-md" type="button" onClick={deleteHandler}>Delete</button>
       
    </div>
  )
}

export default TransactionAction