from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http import HTTPClient

from .user import User


@dataclass(slots=True)
class GuildMember:
    """Represents a member of a guild.

    This combines a User object with guild-specific information like
    nickname, roles, join date, etc.
    """

    # The underlying user
    user: User

    # Guild-specific fields
    nick: str | None = None  # Guild nickname (overrides global_name)
    avatar_hash: str | None = None  # Guild-specific avatar hash
    banner: str | None = None  # Guild-specific banner
    accent_color: int | None = None  # Guild-specific accent color
    roles: list[int] = field(default_factory=list)  # Role IDs (as ints)
    joined_at: str | None = None  # ISO 8601 timestamp

    # Invite/join tracking
    join_source_type: int | None = None
    source_invite_code: str | None = None
    inviter_id: int | None = None

    # Voice state
    mute: bool = False
    deaf: bool = False

    # Moderation
    communication_disabled_until: str | None = None  # Timeout until (ISO 8601)

    # Back-reference (set after construction)
    _http: HTTPClient | None = field(default=None, repr=False)

    @classmethod
    def from_data(
        cls, data: dict[str, Any], http: HTTPClient | None = None
    ) -> GuildMember:
        # Parse the nested user object
        user = User.from_data(data["user"], http)

        return cls(
            user=user,
            nick=data.get("nick"),
            avatar_hash=data.get("avatar"),
            banner=data.get("banner"),
            accent_color=data.get("accent_color"),
            roles=[int(role_id) for role_id in data.get("roles", [])],
            joined_at=data.get("joined_at"),
            join_source_type=data.get("join_source_type"),
            source_invite_code=data.get("source_invite_code"),
            inviter_id=int(data["inviter_id"]) if data.get("inviter_id") else None,
            mute=data.get("mute", False),
            deaf=data.get("deaf", False),
            communication_disabled_until=data.get("communication_disabled_until"),
            _http=http,
        )

    @property
    def display_name(self) -> str:
        """The best display name for this member.

        Priority: guild nickname > global name > username
        """
        return self.nick or self.user.global_name or self.user.username

    @property
    def mention(self) -> str:
        """Return a string that mentions this member."""
        return f"<@{self.user.id}>"

    @property
    def guild_avatar_url(self) -> str | None:
        """URL for the member's guild-specific avatar, if set."""
        if self.avatar_hash:
            ext = "gif" if self.avatar_hash.startswith("a_") else "png"
            # Note: Guild avatar URLs might have a different format
            # Adjust if Fluxer uses a different URL structure
            return f"https://fluxerusercontent.com/guilds/avatars/{self.user.id}/{self.avatar_hash}.{ext}"
        return None

    def __str__(self) -> str:
        """Return the member's display name."""
        return self.display_name
