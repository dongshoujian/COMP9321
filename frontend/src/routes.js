// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
import Person from "@material-ui/icons/Person";
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";
import countGenres from "views/countGenres/countGenres.js";
import countRating from "views/countRating/countRating.js";
import datevssize from "views/datevssize/datevssize.js";
import potentialCustomer from "views/potentialCustomer/potentialCustomer.js";
import similarTop10 from "views/similarTop10/similarTop10.js";
import UserProfile from "views/UserProfile/UserProfile.js";
import Predict from "views/Predict/predict.js";
import TableList from "views/TableList/TableList.js";
import Typography from "views/Typography/Typography.js";
import Icons from "views/Icons/Icons.js";
import NotificationsPage from "views/Notifications/Notifications.js";
// core components/views for RTL layout
import RTLPage from "views/RTLPage/RTLPage.js";
import SignupPage from "views/Signup/SignupPage.js";
import Fingerprint from "@material-ui/icons/Fingerprint";
import LibraryBooks from "@material-ui/icons/LibraryBooks";
import ExitToApp from "@material-ui/icons/ExitToApp";
import LoginPage from "views/Login/LoginPage.js";


if (localStorage.getItem("isLogin")!='1') {
  var dashboardRoutes = 
      [{
        path: "/login",
        name: "Login",
        icon: ExitToApp,
        component: LoginPage,
        layout: "/admin"
      },]
}else{
  var dashboardRoutes = 
    [{
        path: "/dashboard",
        name: "Top five rating games",
        icon: Dashboard,
        component: DashboardPage,
        layout: "/admin"
      },
      {
        path: "/countRating",
        name: "Count ratings",
        icon: Dashboard,
        component: countRating,
        layout: "/admin"
      },
      {
        path: "/countGenres",
        name: "Count different genres",
        icon: Dashboard,
        component: countGenres,
        layout: "/admin"
      },
      {
        path: "/datevssize",
        name: "Trend of date and size",
        icon: Dashboard,
        component: datevssize,
        layout: "/admin"
      },
      {
        path: "/potentialCustomer",
        name: "Largest potential customers",
        icon: Dashboard,
        component: potentialCustomer,
        layout: "/admin"
      },
      {
        path: "/predict",
        name: "Predict",
        icon: LibraryBooks,
        component: Predict,
        layout: "/admin"
      },
      {
        path: "/searchAttribute",
        name: "Search by attribute",
        icon: LibraryBooks,
        component: similarTop10,
        layout: "/admin"
      },
      {
        path: "/user",
        name: "User Profile",
        icon: Person,
        component: UserProfile,
        layout: "/admin"
      },
    ]
  
}



export default dashboardRoutes;
