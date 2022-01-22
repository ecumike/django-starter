from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class MyprojectOIDCAuthenticationBackend(OIDCAuthenticationBackend):
	"""
	Creates and updates a user. Uses info from IBMid.
	"""
	def create_user(self, claims):
		user = super(MyprojectOIDCAuthenticationBackend, self).create_user(claims)

		user.username = claims.get('preferred_username', '')
		user.first_name = claims.get('given_name', '')
		user.last_name = claims.get('family_name', '')
		user.profile.display_name = claims.get('displayName', '')
		user.save()

		return user

	def update_user(self, user, claims):
		user.username = claims.get('preferred_username', '')
		user.first_name = claims.get('given_name', '')
		user.last_name = claims.get('family_name', '')
		user.profile.display_name = claims.get('displayName', '')
		user.save()

		return user
