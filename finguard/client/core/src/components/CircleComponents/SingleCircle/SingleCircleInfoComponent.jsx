import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"
import InfoMemberComponent from "./InfoMemberComponent"
import SingleCircleInfoActionComponent from "./SingleCircleInfoActionComponent"
import { FaEdit } from "react-icons/fa"
import Link from "next/link"


async function fetchCircleInfo(circleId, authToken) {
  const url = "transaction/circle?id=" + circleId
  const res = await sendRequest(url, { providedAuthToken: authToken })
  return res
}



async function SingleCircleInfoComponent({ circleId, authToken, isAdmin, authUserId }) {

  const circleInfoRes = await fetchCircleInfo(circleId, authToken)


  // destructuring ...
  const data = circleInfoRes?.data?.msg || null


  return (
    <div className="flex flex-col">
      {!data ? <h2 className="mx-auto"> {circleInfoRes?.err?.[0]} </h2> : <>

        {/* First */}
        <div className="my-2 mx-auto flex flex-col items-center">
          <MediaPresentationComponent name={data?.name} media={data?.media} />
          
          {isAdmin && 
          <Link className="mb-2 mt-1 text-[1.3em] text-accent-color transition-all duration-300 hover:transform-[scale(1.2)] hover:text-primary-color" href={"/media?type=circle&id="+circleId}> <FaEdit/> </Link>
        }
          <h3 className="poppins-bold text-[1.2em]"> {data?.name}  </h3>
          <p className="my-1 text-center max-w-[400px]"> {data?.description}  </p>
          <small className="font-medium"> {new Date(data?.created_at).toLocaleDateString()}  </small>
          {isAdmin && <SingleCircleInfoActionComponent circleId={circleId}  /> }
        </div>

        {/* Displaying member list only when auth user id is present */}
        {!!authUserId &&
          <InfoMemberComponent authUserId={authUserId} key={data?.members || 1} circleId={circleId} members={data?.members} isAdmin={isAdmin} />
        }
      </>}
    </div>
  )
}

export default SingleCircleInfoComponent