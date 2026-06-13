"use client"
import { FaEdit } from "react-icons/fa"
import Link from "next/link"
import { MdDeleteForever } from "react-icons/md";
import sendRequest from "@/utils/requestSender";
import { useState } from "react";
import FullPageLoadingComponent from "@/components/Others/FullPageLoadingComponent";
import { toast, ToastContainer } from "react-toastify";
import { useRouter } from "next/navigation";

function SingleCircleInfoActionComponent({ circleId }) {
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()


    /**
     * ### This function is responsible for deleting circle
    
     */
    async function circleDeleteHandler() {
        setIsLoading(true)
        const url = "transaction/circle?id=" + circleId
        const res = await sendRequest(url, { method: "DELETE" })
        setIsLoading(false)

        if (!res?.success || res?.err) {
            toast.error(res?.err?.[0])
            return
        }

        toast.success(res?.data?.msg)
        router.replace("/circle")

    }
    return (
        <div className="flex justify-around items-center">
            {isLoading && <FullPageLoadingComponent />}
            <ToastContainer/>
            <Link className="text-center w-fit px-3 py-1 text-[1.7em] my-2 text-primary-color hover:text-emerald-500" href={"/circle/create?id=" + circleId} title="Edit Circle Information"> <FaEdit />  </Link>
            <button onClick={() => { circleDeleteHandler() }}  type="button" className="text-center w-fit px-3 py-1 text-[1.7em] my-2 cursor-pointer text-primary-color hover:text-rose-500" title="Delete Circle"> <MdDeleteForever /> </button>
        </div>
    )
}

export default SingleCircleInfoActionComponent