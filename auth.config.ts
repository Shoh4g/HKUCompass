import { useUserStore } from '@/app/(utils)/providers/user-store-provider';
import { postLogin } from '@/app/api/auth/routes';
import { profilePicList } from '@/app/mockData';
import { NextAuthOptions, User } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

const validateCredentials = async (credentials: { email: string, password: string }): Promise<User | null> => {

  try {
    const res = await postLogin(credentials.email, credentials.password);

    if (res) {
      const userData = res;

      const nextAuthUser: User = {
        id: userData._id,
        name: userData.FULLNAME,
        email: userData.EMAIL,
        image: userData.PROFILE_PIC,
      };

      return nextAuthUser;
    } else {
      return null;
    }
  } catch (err) {
    console.error('Error logging in: ', err);
    throw err;
  }
}

export const authOptions = {
	providers: [
		CredentialsProvider({
      name: 'Credentials',
      async authorize(credentials, req): Promise<User | null> {
        const { email, password } = credentials as { email: string, password: string };

        const user = await validateCredentials({ email, password });

        if (user) {
          return user;
        }
        return null;
      },
      credentials: {
        email: { label: 'Email', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
    }),
	],
  session: {
    strategy: 'jwt',
  },
  jwt: {
    secret: process.env.JWT_SECRET,
  },
  secret: process.env.NEXTAUTH_SECRET,
} satisfies NextAuthOptions;
