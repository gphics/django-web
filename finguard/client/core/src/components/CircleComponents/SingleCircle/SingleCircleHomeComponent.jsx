import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"

async function fetchCircleMembersRanking(circleId, authToken) {
  const url = "transaction/rank-circle-members/" + circleId
  const res = await sendRequest(url, { providedAuthToken: authToken })
  return res
}

async function SingleCircleHomeComponent({ circleId, authToken }) {
  // console.log("This is the home pge")
  // console.log(circleId, authToken)
  const res = await fetchCircleMembersRanking(circleId, authToken)
  const rawData = res?.data?.msg || []

  const data = rawData.map(elem => {
    const user = elem?.user
    const profile = elem?.user?.profile
    const finalProduct = {}
    // filling
    finalProduct.username = user?.username
    finalProduct.rank = elem?.rank
    finalProduct.media = profile?.media
    finalProduct.transaction_count = profile?.number_of_transactions
    finalProduct.currency = profile?.currency
    finalProduct.financial_activity = profile?.financial_activity
    finalProduct.average = profile?.summary_statistics?.mean
    finalProduct.min = profile?.summary_statistics?.min
    finalProduct.max = profile?.summary_statistics?.max
    return finalProduct
  }).sort((a, b) => a?.rank - b?.rank)

  return (
    <div>

      {!res?.success || res?.err ? <h3>{res?.err[0]}</h3> : <>
        <table className="w-full text-[0.9em] max-md:hidden">
          <thead>
            <tr className="bg-accent-color h-10 ">
              <th className="text-start pl-2">Rank</th>
              <th className="text-start pl-2">Username</th>
              <th className="text-start pl-2">Financial Activity</th>
              <th className="text-start pl-2">Transaction Count</th>
              <th className="text-start pl-2">Average</th>
              <th className="text-start pl-2">Min</th>
              <th className="text-start pl-2">Max</th>
            </tr>

          </thead>

          <tbody>
            {data.map((elem, i) => {
              return <tr key={i} className="bg-overlay h-13 ">
                {/* Rank */}
                <td className="text-start pl-2">{elem?.rank}  </td>

                {/* Username and media */}
                <td className="text-start pl-2">
                  <div className="flex items-center">

                    <MediaPresentationComponent name={elem?.username} media={elem?.media} />
                    <h4 className=" ml-2 capitalize">{elem?.username}</h4>
                  </div>
                </td>

                {/* Financial activity */}
                <td className="text-start pl-2">  {elem?.financial_activity} </td>

                {/* Transaction Count */}
                <td className="text-start pl-2"> {elem?.transaction_count}  </td>

                {/* Average */}
                <td className="text-start pl-2">{elem?.currency} {elem?.average}  </td>

                {/* Min */}
                <td className="text-start pl-2"> {elem?.currency} {elem?.min}  </td>

                {/* Max */}
                <td className="text-start pl-2"> {elem?.currency} {elem?.max}  </td>
              </tr>
            })}
          </tbody>
        </table>
        
        <section className="md:hidden mt-5 flex flex-wrap justify-center">
          {data.map((elem, i) => {
            return <div key={i} className="w-fit m-2">
              <h4 className="mx-auto w-[40px] h-[30px] bg-accent-color rounded-t-sm text-center poppins-bold pt-1"> {elem?.rank} </h4>
             <article className="flex flex-col p-4 bg-overlay  rounded-b-sm">
               {/* Username and media */}
               <div className="flex items-center">

                 <MediaPresentationComponent name={elem?.username} media={elem?.media} />
                 <h4 className=" ml-2 capitalize">{elem?.username}</h4>
               </div>

               {/* Financial activity */}
               <p> <strong>Financial Activity :</strong> {elem?.financial_activity}</p>

               {/* Transaction Count */}
               <p> <strong>Transaction Count :</strong> {elem?.transaction_count} </p>

               {/* Average */}
               <p> <strong>Average:</strong> {elem?.currency}{elem?.average} </p>

               {/* Min */}
               <p> <strong>Min: </strong>{elem?.currency} {elem?.min} </p>

               {/* Max */}
               <p> <strong>Max: </strong>{elem?.currency} {elem?.max} </p>
             </article>
            </div>
            

          })}
        </section>



      </>}
    </div>
  )
}

export default SingleCircleHomeComponent