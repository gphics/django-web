"use client"

import { toast, ToastContainer } from "react-toastify"
import MediaPresentationComponent from "../Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"
import { useState } from "react"
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"
import { useRouter } from "next/navigation"

function PendingInvitationComponent({ pendingRes }) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const data = pendingRes?.data?.msg || []

  if (!data.length) {

    toast.error(pendingRes?.err?.[0])
  }
  const responseArr = ["ACCEPTED", "DECLINED"]
  async function invitationReply(inviteId, status = responseArr[0]) {
    setIsLoading(true)

    const url = "transaction/circle-invite"
    const body = { id: inviteId, status }
    const res = await sendRequest(url, { method: "PUT", body })
    setIsLoading(false)
    if (!res?.success || res?.err) {

      toast.err(res?.err[0])
      return
    }

    toast.success(res?.data?.msg)
    router.refresh()

  }
  return (
    <div>
      {!!isLoading &&
        <FullPageLoadingComponent />
      }
      <ToastContainer />

      {data?.length ? <>
        <h2 className="poppins-bold text-[1.3em] text-center mt-4 ">Pending Invitations ({data?.length})  </h2>

        <section className="flex flex-col">
          {data.map((elem, i) => {
            return <article key={i} className="my-2 p-2 w-full max-w-[400px] shadow-md hover:transform-[scale(1.008)] transition-all duration-400">
              <div className="my-1">
                <MediaPresentationComponent name={elem?.circle} media={elem?.circle_media} />
                <h3 className="mt-1 poppins-bold"> {elem?.circle}  </h3>
              </div>
              <div className="my-2 flex justify-between w-[70%]">
                <button onClick={() => {
                  invitationReply(elem?.id, responseArr[0])
                }} type="button" className="bg-emerald-300 px-5 py-1 cursor-pointer poppins-bold  transition-all duration-600 ">Accept</button>
                <button className="bg-rose-300 px-5 py-1 cursor-pointer poppins-bold transition-all duration-600 " onClick={() => {
                  invitationReply(elem?.id, responseArr[1])
                }} type="button">Decline</button>
              </div>
            </article>
          })}
        </section>
      </> :
        <h2 className="text-center my-10 text-[1.5em] poppins-bold text-primary-color capitalize">You have no pending invitations</h2>
      }

    </div>
  )
}

export default PendingInvitationComponent