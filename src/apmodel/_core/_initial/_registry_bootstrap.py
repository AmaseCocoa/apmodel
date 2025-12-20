from ...extra.cid.data_integrity_proof import DataIntegrityProof
from ...extra.cid.multikey import Multikey
from ...extra.emoji import Emoji
from ...extra.hashtag import Hashtag
from ...extra.litepub.emoji_react import EmojiReact
from ...extra.schema.propertyvalue import PropertyValue
from ...extra.security.cryptographickey import CryptographicKey
from ...vocab.activity.accept import Accept, TentativeAccept
from ...vocab.activity.add import Add
from ...vocab.activity.announce import Announce
from ...vocab.activity.arrive import Arrive
from ...vocab.activity.block import Block
from ...vocab.activity.create import Create
from ...vocab.activity.delete import Delete
from ...vocab.activity.dislike import Dislike
from ...vocab.activity.flag import Flag
from ...vocab.activity.follow import Follow
from ...vocab.activity.ignore import Ignore
from ...vocab.activity.invite import Invite
from ...vocab.activity.join import Join
from ...vocab.activity.leave import Leave
from ...vocab.activity.like import Like
from ...vocab.activity.listen import Listen
from ...vocab.activity.move import Move
from ...vocab.activity.offer import Offer
from ...vocab.activity.question import Question
from ...vocab.activity.read import Read
from ...vocab.activity.reject import Reject, TentativeReject
from ...vocab.activity.remove import Remove
from ...vocab.activity.travel import Travel
from ...vocab.activity.undo import Undo
from ...vocab.activity.update import Update
from ...vocab.activity.view import View
from ...vocab.actor import (
    Application,
    Group,
    Organization,
    Person,
    Service,
)
from ...vocab.article import Article
from ...vocab.document import Audio, Document, Image, Page, Video
from ...vocab.event import Event, Place
from ...vocab.mention import Mention
from ...vocab.note import Note
from ...vocab.profile import Profile
from ...vocab.tombstone import Tombstone

TYPE_MAPPING = {
    "http://joinmastodon.org/ns#Emoji": Emoji,
    "https://www.w3.org/ns/activitystreams#Hashtag": Hashtag,
    "https://w3id.org/security#DataIntegrityProof": DataIntegrityProof,
    "https://www.w3.org/ns/cid/v1#Multikey": Multikey,
    "https://w3id.org/security#Key": CryptographicKey,
    "https://www.w3.org/ns/activitystreams#Application": Application,
    "https://www.w3.org/ns/activitystreams#Group": Group,
    "https://www.w3.org/ns/activitystreams#Organization": Organization,
    "https://www.w3.org/ns/activitystreams#Person": Person,
    "https://www.w3.org/ns/activitystreams#Service": Service,
    "https://www.w3.org/ns/activitystreams#Article": Article,
    "https://www.w3.org/ns/activitystreams#Document": Document,
    "https://www.w3.org/ns/activitystreams#Audio": Audio,
    "https://www.w3.org/ns/activitystreams#Image": Image,
    "https://www.w3.org/ns/activitystreams#Video": Video,
    "https://www.w3.org/ns/activitystreams#Page": Page,
    "https://www.w3.org/ns/activitystreams#Event": Event,
    "https://www.w3.org/ns/activitystreams#Place": Place,
    "https://www.w3.org/ns/activitystreams#Mention": Mention,
    "https://www.w3.org/ns/activitystreams#Note": Note,
    "https://www.w3.org/ns/activitystreams#Profile": Profile,
    "https://www.w3.org/ns/activitystreams#Tombstone": Tombstone,
    "https://www.w3.org/ns/activitystreams#Accept": Accept,
    "https://www.w3.org/ns/activitystreams#TentativeAccept": TentativeAccept,
    "https://www.w3.org/ns/activitystreams#Add": Add,
    "https://www.w3.org/ns/activitystreams#Announce": Announce,
    "https://www.w3.org/ns/activitystreams#": Arrive,
    "https://www.w3.org/ns/activitystreams#Ignore": Ignore,
    "https://www.w3.org/ns/activitystreams#Block": Block,
    "https://www.w3.org/ns/activitystreams#Create": Create,
    "https://www.w3.org/ns/activitystreams#Delete": Delete,
    "https://www.w3.org/ns/activitystreams#Dislike": Dislike,
    "https://www.w3.org/ns/activitystreams#Flag": Flag,
    "https://www.w3.org/ns/activitystreams#Follow": Follow,
    "https://www.w3.org/ns/activitystreams#Offer": Offer,
    "https://www.w3.org/ns/activitystreams#Invite": Invite,
    "https://www.w3.org/ns/activitystreams#Join": Join,
    "https://www.w3.org/ns/activitystreams#Leave": Leave,
    "https://www.w3.org/ns/activitystreams#Like": Like,
    "https://www.w3.org/ns/activitystreams#Listen": Listen,
    "https://www.w3.org/ns/activitystreams#Move": Move,
    "https://www.w3.org/ns/activitystreams#Question": Question,
    "https://www.w3.org/ns/activitystreams#Read": Read,
    "https://www.w3.org/ns/activitystreams#Reject": Reject,
    "https://www.w3.org/ns/activitystreams#TentativeReject": TentativeReject,
    "https://www.w3.org/ns/activitystreams#Remove": Remove,
    "https://www.w3.org/ns/activitystreams#Travel": Travel,
    "https://www.w3.org/ns/activitystreams#Undo": Undo,
    "https://www.w3.org/ns/activitystreams#Update": Update,
    "https://www.w3.org/ns/activitystreams#View": View,
    "http://litepub.social/ns#EmojiReact": EmojiReact,
    "http://schema.org#PropertyValue": PropertyValue,
}
