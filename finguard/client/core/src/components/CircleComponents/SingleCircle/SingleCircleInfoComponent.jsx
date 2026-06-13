import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"
import InfoMemberComponent from "./InfoMemberComponent"
import SingleCircleInfoActionComponent from "./SingleCircleInfoActionComponent"


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