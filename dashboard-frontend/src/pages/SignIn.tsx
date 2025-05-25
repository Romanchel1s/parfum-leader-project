import { AppProvider } from '@toolpad/core/AppProvider';
import { SignInPage, type AuthProvider } from '@toolpad/core/SignInPage';
import { useTheme } from '@mui/material/styles';
import supabase from "../api/supabaseClient";
import { NavigateFunction, useNavigate } from 'react-router-dom';


// preview-start
const providers = [{ id: 'credentials', name: 'Email and Password' }];
// preview-end



const signIn: (provider: AuthProvider, formData: FormData, navigate: NavigateFunction, callbackUrl?: string) => void = (
  _provider,
  formData,
  navigate,
  callbackUrl = "/",
) => {
  const promise = new Promise<void>((resolve) => {
    const signInAsync = async () => {
      const email = formData.get("email") as string;
      const password = formData.get("password") as string;

      const { error } = await supabase.auth.signInWithPassword({ email, password });

      if (error) {
        alert(`Ошибка входа: ${error.message}`);
      } else {
        navigate(callbackUrl)
      }
      resolve();
    };

    signInAsync();
  });
  return promise;
};

export default function CredentialsSignInPage() {
  const navigate = useNavigate();
  const theme = useTheme();
  return (
    // preview-start
    <AppProvider theme={theme}>
      <SignInPage
        signIn={(provider, formData, callbackUrl) => signIn(provider, formData, navigate,  callbackUrl)}
        providers={providers}
        slotProps={{ emailField: { autoFocus: false }, form: { noValidate: true }, rememberMe: { sx: { display: 'none' } } }}
      />
    </AppProvider>
    // preview-end
  );
}
