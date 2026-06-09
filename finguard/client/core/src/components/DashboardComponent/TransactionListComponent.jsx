"use client"
import sendRequest from "@/utils/requestSender";
import { useRouter } from "next/navigation";
import { useState , useEffect} from "react";
import { BiSolidInfoCircle } from "react-icons/bi";
import { toast } from "react-toastify";
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent";
/**
 * 
 * @param {{transactions:Array}} param0 
 * @returns 
 */
function TransactionListComponent({ transactions, currencyRes, transactionCount }) {
    const { data = {}, err = null } = currencyRes
    const [isLoading, setIsLoading] = useState(false)

    const router = useRouter()
    if (err) {
        toast.error(err[0], { toastId: "error-msg" })
    }
    const { currency } = data?.msg

    // const transactionData = transactions

    const [transactionData, setTransactionData] = useState(transactions)
    // console.log(transactionData)
    // useEffect(() => {
    //     setTransactionData(transactions)
    // }, [transactions])

    function toSingleTransaction(id) {
        router.push("/transaction/" + id)
    }

    async function anomalyDetection() {
        setIsLoading(true)
        const url = "transaction/detect-anomaly"
        const res = await sendRequest(url)

        if (res?.err || !res?.success) {
            toast.error(res?.err[0])
            return
        }

        const { is_anomalous, resultStr } = res?.data?.msg

        if (is_anomalous) {
            // fetching updated transactions
            const updatedTransactions = await sendRequest("transaction/?page=1")
            setTransactionData(updatedTransactions?.data?.transactions)
        }

        // notification ...
        setIsLoading(false)
        toast.success(resultStr)


    }
    return (
        <div className="flex flex-col">
            {!!isLoading && <FullPageLoadingComponent />}


            {transactionData.length ? <>

                {/* Header */}
                <section className="flex justify-around max-w-[500px] w-full self-center mx-2 items-center">

                    <h3 className='poppins-bold text-center my-2'>My Transactions ({transactionCount}) </h3>

                    <button type="button" className="bg-emerald-400 px-3 py-1 cursor-pointer hover:bg-rose-400 transition-all durationn-300 rounded-sm poppins-bold" onClick={anomalyDetection}>Detect Anomaly</button>
                </section>

                {/* Data Table */}
                <table className='w-full border-collapse table-auto my-2'>

                    <thead className='bg-gray-200 text-[.9em]'>
                        <tr>
                            <th className='py-2 text-start text-gray-800'>Category</th>
                            <th className='py-2 text-start'>Amount({currency})  </th>
                            <th className='py-2 text-start'>Anomalous</th>
                            <th className='py-2 text-start'>Detail</th>
                        </tr>

                    </thead>

                    <tbody className='divide-y'>
                        {transactionData.map((item, index) => {
                            const rowColor = item.flagged ? "bg-rose-200" : "bg-emerald-200"

                            return <tr key={index} className={`transition-transform ${rowColor} hover:scale-[1.001] text-[.9em]`} >
                                <td className='py-3 px-1 '> {item.category} </td>
                                <td> {item.amount}  </td>
                                <td className={'capitalize'}>  {String(item.flagged)} </td>

                                {/* link to single transaction */}
                                <td className="text-center text-[1.5em] cursor-pointer hover:text-blue-600" onClick={() => toSingleTransaction(item.id)}> <BiSolidInfoCircle /></td>
                            </tr>
                        })}
                    </tbody>
                </table>
            </> : <h2 className="self-center my-10 poppins-bold capitalize text-[1.2em]">You have no transaction</h2>}
        </div>
    )
}

export default TransactionListComponent