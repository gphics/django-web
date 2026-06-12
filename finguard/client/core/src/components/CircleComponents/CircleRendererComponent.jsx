"use client"

import { useState } from "react"
import PendingInvitationComponent from "./PendingInvitationComponent"
import CircleListComponent from "./CircleListComponent"
import Link from "next/link"
import { ToastContainer } from "react-toastify"

function CircleRendererComponent({ circleRes, pendingRes }) {


  const [isPending, setIsPending] = useState(false)
  return (
    <div className="flex flex-col">
      <ToastContainer/>
      {/* Navigator */}
      <section className="flex self-center justify-between w-full max-w-[350px] ">

        <button type="button" className={`px-4 py-1 cursor-pointer hover:bg-accent-color transition-all duration-300 ${!isPending ? "bg-accent-color" : "bg-overlay"}`} onClick={(e) => setIsPending(false)}>Circle</button>
        <button type="button" className={`px-4 py-1 cursor-pointer hover:bg-accent-color transition-all duration-300 ${isPending ? "bg-accent-color" : "bg-overlay"}`} onClick={(e) => setIsPending(true)}>Pending</button>


      </section>
      {isPending ? <PendingInvitationComponent /> : <section className="flex justify-around flex-wrap  my-2 items-cennter">
        <div className="w-[130px] flex flex-col justify-center items-center h-[130px] bg-overlay rounded-sm m-1 hover:bg-accent-color transition-all duration-300">
          <Link href="/circle/create"  className=" h-10 w-10 poppins-bold text-[1.5em] rounded-full bg-white text-center cursor-pointer">+</Link>
          <h4 className="mt-2">Create Circle</h4>
          
        </div>
        
        {/* listing users circles */}
        <CircleListComponent circleRes={circleRes} />
      </section>}
    </div>
  )
}

export default CircleRendererComponent