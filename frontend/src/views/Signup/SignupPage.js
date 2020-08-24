import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Paper from "@material-ui/core/Paper";
import API from "../api";
import {message} from 'antd';
const api = new API();

function signup_submit(){
    const first_name_value = document.getElementById('firstName').value;
    const last_name_value = document.getElementById('lastName').value;
    const email_value = document.getElementById('email').value;
    const password_value = document.getElementById('password').value;
    const password_confirm_value = document.getElementById('password_confirm').value;

    if (password_value != password_confirm_value){
        message.error("Different Passwords");
        return 0
    }

    const path = 'auth/signup';
    const headers = {
        Accept: "application/json",
        "Content-Type": "application/json"
    }
    const method = "POST";
    const body = {
        "email": email_value,
        "password": password_value,
        "first_name":first_name_value,
        "last_name":last_name_value
    }
    api.apiRequest(path,{
        headers,
        method,
        body: JSON.stringify(body)
    }).then(function (res) {
        localStorage.clear()
        localStorage.setItem('isLogin','1')
        localStorage.setItem('userName', JSON.stringify(res.result));
        console.log(res)
        message.success('Successfully Signup')
        setTimeout("window.location.href='/login'", 1000)

    //     if (res.result == 'Invalid email or password'){
    //         message.error('Wrong Password');
    //     }
    //     else{
    //         localStorage.setItem('isLogin','1')
    //         message.success('Successfully Login')
    //         setTimeout("window.location.href='/'", 1000)
    //     }
    })
}


function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://material-ui.com/">
                ROUND TABLE 9321
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const useStyles = makeStyles(theme => ({
    root: {
        height: '100vh',
    },
    image: {
        backgroundImage: 'url(https://source.unsplash.com/random)',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    },
    paper: {
        margin: theme.spacing(8, 4),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

export default function SignupPage() {
    const classes = useStyles();

    return (
            <Grid item xs={12} sm={8} md={12} component={Paper} elevation={6} square>
                <div className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign up
                    </Typography>
                    <form className={classes.form} noValidate>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    autoComplete="fname"
                                    name="firstName"
                                    variant="outlined"
                                    required
                                    fullWidth
                                    id="firstName"
                                    label="First Name"
                                    autoFocus
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    id="lastName"
                                    label="Last Name"
                                    name="lastName"
                                    id = "lastName"
                                    autoComplete="lname"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    id="email"
                                    label="Email Address"
                                    id = "email"
                                    name="email"
                                    autoComplete="email"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    name="password1"
                                    label="Password"
                                    type="password"
                                    id="password"
                                    autoComplete="current-password"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    name="password2"
                                    label="Confirm Password"
                                    type="password"
                                    id="password_confirm"
                                    autoComplete="current-password"
                                />
                            </Grid>
                        </Grid>
                        <Button
                            // type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            // className={classes.submit}
                            onClick={() => signup_submit()}
                            style={{marginTop:"15px"}}
                        >
                            Sign Up
                        </Button>
                        <Grid container justify="flex-end">
                            <Grid item style={{marginTop:"15px"}}>
                              <Box mt={5}>
                                <Copyright />
                              </Box>
                            </Grid>
                        </Grid>
                    </form>
                </div>
            </Grid>
    );
}