// import ChatPage from "./pages/ChatPage";

// // import AppShell from "./app/AppShell";
// // import AppRoutes from "./app/routes";
// // import Providers from "./app/providers";
// // export default function App() {
// //   return <ChatPage />;
// //     <Providers>
// //       <AppShell>
// //         <AppRoutes />
// //       </AppShell>
// //     </Providers>

// // }
// import AppShell from "./app/AppShell";
// import AppRoutes from "./app/routes";
// import Providers from "./app/providers";

// export default function App() {
//   return (
//     <>
//       <ChatPage />
//       <Providers>
//         <AppShell>
//           <AppRoutes />
//         </AppShell>
//       </Providers>
//     </>
//   );
// }
import AppShell from "./app/AppShell";
import AppRoutes from "./app/routes";
import Providers from "./app/providers";

export default function App() {
  return (
    <Providers>
      <AppShell>
        <AppRoutes />
      </AppShell>
    </Providers>
  );
}
