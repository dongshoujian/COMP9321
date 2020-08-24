import React, { Component } from 'react'
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Store from "@material-ui/icons/Store";
import Warning from "@material-ui/icons/Warning";
import DateRange from "@material-ui/icons/DateRange";
import LocalOffer from "@material-ui/icons/LocalOffer";
import Update from "@material-ui/icons/Update";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import AccessTime from "@material-ui/icons/AccessTime";
import Accessibility from "@material-ui/icons/Accessibility";
import BugReport from "@material-ui/icons/BugReport";
import Code from "@material-ui/icons/Code";
import Cloud from "@material-ui/icons/Cloud";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Tasks from "components/Tasks/Tasks.js";
import CustomTabs from "components/CustomTabs/CustomTabs.js";
import Danger from "components/Typography/Danger.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import tesdImage from "assets/img/cover.jpeg";
import ReactSVG from 'react-svg'
import { Avatar } from '@material-ui/core';
import ImageIcon from '@material-ui/icons/Image';
import { bugs, website, server } from "variables/general.js";

import {
  dailySalesChart,
  emailsSubscriptionChart,
  completedTasksChart
} from "variables/charts.js";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import API from "../api.js";
const api = new API();
const useStyles = makeStyles(styles);

export default class Dashboard extends Component{

  constructor(props) {
    super(props);
    this.state = {
      isLoading:true,
      topFive:[],
      avgUserRating:null,
      dateVsAppSize:null,
      category:null,
      countGeners:null,
    };

    
  }

  async componentWillMount() {
    const token = localStorage.getItem('token')
    var path = 'getTopFive';
    // console.log(path)
    var headers = {
      Accept: "application/json",
      "Content-Type": "application/json",

      "AUTH-TOKEN": token,
    }
    const method = "GET";
    
    path = 'dateVsAppSize';
    await api.apiRequest(path, {
        headers,
        method,
      }).then((res) => {
        console.log(res.result)
        this.setState({
          dateVsAppSize: require('./dateVsAppSize.svg')
        })
      });
    path = 'avgUserRating';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        avgUserRating: require('./avgUserRating.svg')
      })
    });
    path = 'category';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        categoryChart: require('./categoryChart.svg')
      })
    });
    path = 'countGeners';
    await api.apiRequest(path, {
      headers,
      method,
    }).then((res) => {
      console.log(res.result)
      this.setState({
        countGeners: require('./countGeners.svg')
      })
    });
    // console.log(result)
    this.setState({isLoading:false})
    
    };

  render(){
    const { isLoading, ...res} = this.state;
        if (isLoading) {
            return (<div> Loading
            </div>
            )
        }
    return (

      <div>

        < GridContainer direction = "column"
        alignItems = "center"
        justify = "center" >
          <GridItem xs={12} sm={12} md={7}>
          <Card>
        <CardActionArea>
          <ReactSVG src = {this.state.dateVsAppSize} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Date & APP Size
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              With the development of technology, the size of game app is becoming larger and larger.
            </Typography>
          </CardContent>
        </CardActionArea>
      
      </Card>
          </GridItem>
        </GridContainer>
      </div>
    );
  }

  }