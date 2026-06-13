import TransactionAction from "./TransactionAction"

function SingleTransactionComponent({ data, currencyRes }) {
  return (
    <div className='flex flex-col w-full'>
      <h2 className="poppins-bold text-center my-2">Transaction Details</h2>
      {/* Important Transaction Details */}
      <FirstPart flagged={data?.flagged} category={data?.category} transaction_type={data?.transaction_type} />

      {/* Transaction Details */}
      <SecondPart description={data?.description} transaction_date={data?.transaction_date} created_at={data?.created_at} updated_at={data?.updated_at} />

      {/* Location Details */}
      <LocationData city={data?.city} state={data?.state} country={data?.country} />


      {/* Amount data */}
      <AmountData flagged={data?.flagged} currency={currencyRes?.data?.msg?.currency} amount={data?.amount} />

      {/* Transaction Action */}
      <TransactionAction id={data?.id} />

    </div>
  )
}

function FirstPart({ flagged, category, transaction_type }) {
  return <section className='flex flex-col my-1 items-end'>

    {/* flagged */}
    <article className="my-1 mr-5 min-w-[40%]">
      <small>Flag</small>
      {flagged ? <h4 className='text-rose-400 poppins-bold'>Anomaly</h4> : <h4 className='text-emerald-400 poppins-bold'>Normal</h4>}
    </article>

    {/* category */}
    <article className="my-1 mr-5 min-w-[40%]">
      <small> category </small>
      <h3 className="poppins-bold">  {category} </h3>
    </article>

    {/* Transaction Type */}

    <article className="my-1 mr-5 min-w-[40%]">
      <small> Transaction Type </small>
      <h4 className={transaction_type === "DEBIT" ? "text-rose-400" : "text-emerald-400"}>  <span className="poppins-bold">{transaction_type}</span> </h4>

    </article>

  </section>
}

function SecondPart({ description, transaction_date, created_at, updated_at }) {


  const transactionDate = new Date(transaction_date)
  const createdAt = new Date(created_at)
  const updatedAt = new Date(updated_at)


  return <div className='flex flex-col'>

    {/* description */}
    <article className="my-1">
      <small className="poppins-bold">
        Description
      </small>
      <p>
        {description}
      </p>
    </article>

    {/* Dates */}
    <DatePresentation date={transactionDate} title={"Transaction Date"} />
    <DatePresentation date={createdAt} title={"Created At"} />
    <DatePresentation date={updatedAt} title={"Updated At"} />

  </div>
}

function DatePresentation({ date, title }) {
  return <article className="my-1">

    <small className="poppins-bold">
      {title}
    </small>
    <h5 className="text-[.9em]">
      {date.toDateString()}
    </h5>
    <h6>
      {date.toLocaleTimeString()}
    </h6>
  </article>
}

function LocationData({ city, state, country }) {
  return <article className="my-1">
    <small className="poppins-bold">Location</small>

    <p> {city} {state} , {country}  </p>
  </article>
}

function AmountData({ currency, amount, flagged }) {

  return <article className="my-1 min-w-[40%] self-end">
    <small>
      Amount
    </small>

    <h3 className={`poppins-bold ${flagged ? "text-rose-500" : "text-emerald-500"}`} >
      {currency} {amount}
    </h3>
  </article>
}
export default SingleTransactionComponent