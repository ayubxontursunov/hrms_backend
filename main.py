# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth.hashers import make_password
# import random
# import string
#
# class UserCreateView(APIView):
#     def generate_random_password(self, length=12):
#         characters = string.ascii_letters + string.digits + string.punctuation
#         return ''.join(random.choice(characters) for i in range(length))
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Generate random password
#             random_password = self.generate_random_password()
#
#             # Encode the password
#             password_hash = make_password(random_password)
#
#             # Save the user with the encoded password
#             user = serializer.save(password_hash=password_hash)
#
#             # Return the generated password in the response
#             return Response({
#                 'message': 'User created successfully',
#                 'username': user.username,
#                 'email': user.email,
#                 'generated_password': random_password
#             }, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, *args, **kwargs):
#         try:
#             user = User.objects.get(id=kwargs.get('user_id'))
#         except User.DoesNotExist:
#             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True allows for partial updates
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         try:
#             user = User.objects.get(id=kwargs.get('user_id'))
#         except User.DoesNotExist:
#             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         user.delete()
#         return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#
#
# from django.urls import path
# from .views import UserCreateView
#
# urlpatterns = [
#     # Route for creating a user
#     path('users/', UserCreateView.as_view(), name='user-create'),
#
#     # Route for updating or deleting a user
#     path('users/<int:user_id>/', UserCreateView.as_view(), name='user-detail'),
# ]

from django.contrib.auth.hashers import PBKDF2PasswordHasher

# This is the class that Django uses for PBKDF2_SHA256 hashing
class PBKDF2SHA256PasswordHasher(PBKDF2PasswordHasher):
    iterations = 600000

def verify_password(plaintext_password, hash_string):
    hasher = PBKDF2SHA256PasswordHasher()
    # Extract the hash components
    algorithm, iterations, salt, hash_value = hash_string.split('$')
    hasher.iterations = int(iterations)
    # Recompute the hash with the provided plaintext password and compare
    return hasher.verify(plaintext_password, hash_string)

# Example usage
hash_string = 'pbkdf2_sha256$600000$xdT6Eu14vWxyJNPsI0BM6q$5gmHcZUH6ne0O9UuUebkcu2PCk3K++qpxBWYIkVRxd4='
plaintext_password = 'mypassword'

is_correct = verify_password(plaintext_password, hash_string)
print("Password is correct:", is_correct)
