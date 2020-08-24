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
import { Col,  Form, FormGroup, Label, Input, FormText } from 'reactstrap';


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
      topTen:[],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    // this.getPrediction= this.getPrediction.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    })
    console.log(this.state)
    // console.log(this.state.value)
  }
  handleSubmit = event => {
    event.preventDefault();
    const token = localStorage.getItem('token')
    var path = 'searchAttribute';
    const method = 'POST';
    var headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
      "AUTH-TOKEN":token,
    }
    const body = {
      "price": this.state.Price,
      "ageRating": this.state.ageRating,
      "genres": this.state.genres,
    }
    console.log(body)
    api.apiRequest(path, {
      headers,
      method,
      body: JSON.stringify(body)
    }).then((res) => {
      console.log(res.result);
      var result  = [];
      res.result.forEach(element => {
        let resultObj = [];
        let icon = <CardMedia>
          < Avatar src={element["Icon URL"]} alt="..." />
          </CardMedia>
        // console.log(element["Icon URL"]);
        let name = element["Name"];
        let rating = element["AverageUserRating"];
        let genres = element["Genre"];
        let size = element["Size"];
        let price = element["Price"];
        let age = element["AgeRating"];
        resultObj = [icon,name,genres,price,size,rating,age]
        result.push(resultObj);
      })
      this.setState({topTen:result})
      console.log(this.state.topTen)
      //  console.log(res)
    })

  }

  render(){
    const category = 'Action, Adventure, Board, Books, Business, Card, Casino, Casual, Education, Entertainment, Family, Finance, Food&Drink, Health&Fitness, Lifestyle, Magazines&Newspapers, Medical, Music, Navigation, News, Photo&Video, Productivity, Puzzle, Racing, Reference, RolePlaying, Shopping, Simulation, SocialNetworking, Sports, Stickers, Strategy, Travel, Trivia, Utilities, Word';
    const age = 'Age_12+, Age_17+, Age_4+, Age_9+';
    return (

      <div>
        <Form onSubmit={this.handleSubmit}>

       
      <GridContainer className="justify-content-center">
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader >
              <h4 className={useStyles.cardTitleWhite}>Model Prediction</h4>
    
            </CardHeader>
            <CardBody  style = {{fontSize:'20px'}}>
              <GridContainer >
               
                <GridItem xs={12} sm={12} md={5}>
                < FormText >*Price </ FormText>
                <Input
                    id="Price"
                    name="Price" 
                    required
                    // value={this.state.Price} 
                    onChange={this.handleChange}
                 
                  />
            
                </GridItem>
                <GridItem xs={12} sm={12} md={5}>
                    < FormText>*ageRating </ FormText>

                  <Input
                    required 
                    id="ageRating"
                    name="ageRating" 
                    // value={this.state.value} 
                    onChange={this.handleChange}
                 
                  />
                </GridItem>
               
              </GridContainer>
              <br>
              </br>
              <GridContainer>
                <GridItem xs={12} sm={12} md={5}>
                < FormText>*Genres </ FormText>
                <Input
                
                    id="genres"
                    name="genres"
                    required
                    onChange={this.handleChange}
                 
                  />
                </GridItem>
                <GridItem xs={12} sm={12} md={12}><p>Genres should be selected from following list:</p>
                </GridItem>
                <GridItem xs={12} sm={12} md={12}>{category}
                </GridItem>
                <GridItem xs={12} sm={12} md={12} ><p>ageRating should be selected from following list:</p>
                </GridItem>
                <GridItem xs={12} sm={12} md={12}>{age}
                </GridItem>
              </GridContainer>
           </CardBody>
           
           <Button type="submit" >Start Searching</Button>
          </Card>

          </GridItem >
  
                    </GridContainer> 
                    </Form>
        <GridContainer>   
          <GridItem xs={12} sm={12} md={12}>
            <Card>
              <CardHeader color="warning">
                <h4 className={useStyles.cardTitleWhite}>The top ten games in selected attribute</h4>
                <p className={useStyles.cardCategoryWhite}>
                </p>
              </CardHeader>

              <CardBody>
                <Table
                  tableHeaderColor="warning"
                  tableHead={["Logo", "Name", "Genres","Price", "Size (bytes)","Age rating","Average User Rating",]}
                  tableData={this.state.topTen}
                />
              </CardBody>
            </Card>
          </GridItem>
        </GridContainer>
      </div>
    );
  }

  }