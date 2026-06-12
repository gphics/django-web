
import sendRequest from '@/utils/requestSender'
import MemberInvitationClientComponent from './MemberInvitationClientComponent'
import CirclePendingInvitationComponent from './CirclePendingInvitationComponent'

async function fetchCirclePendingInvitation(circleId, authToken) {
  const url = "transaction/circle-invite?circle=" + circleId
  const res = await sendRequest(url, { providedAuthToken: authToken })
  return res
}

async function MemberInvitationComponent({ circleId, authToken }) {

  const pendingCircleInvites = await fetchCirclePendingInvitation(circleId, authToken)
  const fullKey = pendingCircleInvites?.data?.msg.length || 1

  
  return (
    <div>
      <CirclePendingInvitationComponent key={fullKey}  circleId={circleId} pendingCircleInvites={pendingCircleInvites} />
      <MemberInvitationClientComponent />
    </div>
  )
}

export default MemberInvitationComponent