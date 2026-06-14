import MediaUploadComponent from "@/components/Others/MediaUploadComponent"


export async function generateMetadata({ searchParams }) {
  const { type } = await searchParams

  return {
    title: type + " media upload"
  }
}

async function page({ searchParams }) {
  const { type, id } = await searchParams
  return (
    <div className="px-2 flex-auto flex flex-col my-1 items-center">
      <h2 className="text-center uppercase font-medium text-[1.2em] my-1">Upload {type} media</h2>
      <MediaUploadComponent type={type} id={id} />
    </div>
  )
}

export default page