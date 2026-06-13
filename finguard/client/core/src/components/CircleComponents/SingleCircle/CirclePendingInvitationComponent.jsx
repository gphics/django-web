"use client"
import FullPageLoadingComponent from '@/components/Others/FullPageLoadingComponent'
import MediaPresentationComponent from '@/components/Others/MediaPresentationComponent'
import sendRequest from '@/utils/requestSender'
import { useEffect, useState } from 'react'
import { toast, ToastContainer } from 'react-toastify'

function CirclePendingInvitationComponent({ pendingCircleInvites, circleId }) {

  const displayLimit = 4
  const [isLoading, setIsLoading] = useState(false)
  const [pendingInvites, setPendingInvites] = useState(pendingCircleInvites?.data?.msg || [])
  const [inviteData, setInviteData] = useState(pendingInvites.slice(0, displayLimit) || [])
  const errorMsg = pendingInvites.length ? null : pendingCircleInvites?.err?.[0]

  useEffect(() => {
    if (errorMsg) {
      toast.error(errorMsg, { toastId: errorMsg })
    }
  }, [errorMsg])


  
  /**
   * This function is responsible for deleting circle invite
   * @param {int} inviteId 
   * @returns 
   */
  async function withdrawInvite(inviteId) {
    setIsLoading(true)
    const url = "transaction/circle-invite?id=" + inviteId
    const res = await sendRequest(url, { method: "DELETE" })
    setIsLoading(false)

    if (!res?.success || res?.err) {
      toast.error(res?.err[0], { toastId: inviteId })

      return
    }

    await fetchInvites()
    
  }

  /**
   * This function is for fetching circle invites after a successful delete
   */
  async function fetchInvites() {
    setIsLoading(true)
    const url = "transaction/circle-invite?circle=" + circleId
    const res = await sendRequest(url)
    setIsLoading(false)

    if (!res?.success || res?.err) {
      toast.error(res?.err[0], { toastId: circleId })

      return
    }
    const freshInvites = res?.data?.msg

    // performing state update ...
    setPendingInvites(freshInvites)

    setInviteData(freshInvites.slice(0,3))
  }
  return (
    <div className='my-1 flex flex-col w-fit'>
      {isLoading && <FullPageLoadingComponent/>}
      <ToastContainer theme='dark' position='top-center' />

      {!errorMsg && <>

        <h2 className='poppins-bold my-1 text-center text-[1.2em] uppercase'>Pending Invites ({pendingInvites.length})</h2>

        <section className='my-1 flex flex-wrap justify-around'>
          {inviteData.map((elem, i) => {
            return <article key={i} className='flex flex-col justify-center my-2 px-2 shadow-md w-[300px] h-[120px] bg-overlay tranition-all duration-300 mx-1'>
              <div className='mb-2 flex justify-between items-center'>
                <MediaPresentationComponent media={elem?.media} name={elem?.user} />
                <h4 className='capitalize text-start  flex-auto ml-2'>{elem?.user}</h4>
              </div>
              <button className='px-4 py-1 bg-rose-400 rounded-sm cursor-pointer hover:poppins-bold w-fit' type="button" onClick={() => withdrawInvite(elem?.id)}>Withdraw Invite</button>
            </article>
          })}
        </section>

        {/* Pending invite display button */}

        {/* Less btn */}
        {pendingInvites.length > displayLimit && <>
          {inviteData?.length > displayLimit && <button onClick={() => setInviteData(pendingInvites.slice(0, displayLimit))} type="button" className='px-3 py-1 bg-accent-color mx-auto cursor-pointer poppins-bold'>See Less</button>}

        {/* More btn */}
          {inviteData?.length < pendingInvites?.length && <button type="button" onClick={() => setInviteData(pendingInvites)} className='px-3 py-1 bg-accent-color mx-auto cursor-pointer poppins-bold'>See More</button>}
        </>}

      </>}
    </div>
  )
}

export default CirclePendingInvitationComponent