# Select your package library ---
#.libPaths("C://Program Files//R//R-3.5.1//library)

#Load packages
library(shiny)
library(dplyr)

#Load database
 July <- read.csv("quater.csv", stringsAsFactors = FALSE)
# July <- July[!July$Signal_strength == "na" , ]
# July <- na.omit(July)
#For non-scientific notation on axes
options(scipen = 999)

ui <- fluidPage(titlePanel("TRAI 2018 Quarterly Data"),
                sidebarLayout(
                  sidebarPanel(
                    #Operator drop down menu
                    fluidRow(
                      selectInput("Operator" , "Select Operator --" , as.list(unique(July$Operator)))
                    ),
                    # Areas drop down menu
                    fluidRow(
                      selectInput("Area" , "Select License Service Area --" , as.list(unique(July[July$Operator == "AIRTEL" ,"LSA"])))
                    ),
                    # Select Download or Upload
                    fluidRow(
                      radioButtons("Type" , "Select Type --" , choices = list("Data Speed" = "Data_speed", "Signal Strength" = "Signal_strength"))
                    ),
                    # fluidRow(
                    #   selectInput("Technology" , "Select Technology --" , as.list(unique(July$Technology)))
                    # ),
                    fluidRow(
                      radioButtons("Technology" , "Select Technology --" , choices = list("4G" = "4G", "3G" = "3G"))
                    ),
                    # Slider to choose number of bins
                    fluidRow(
                      sliderInput("Bins" , "Select Number of Bins --" , min = 5, max = 50, step = 5, value = 20)
                    )
                  ),
                  mainPanel(
                    #Plot Data Speed histogram
                    fluidRow(
                      column(plotOutput("histUploadplot", height = 300), width = 12)
                    ),
                    fluidRow(
                      htmlOutput("uploadInfo")
                    ),
                    #Plot Signal Strength histogram
                    fluidRow(
                      column(plotOutput("histDownloadplot", height = 300), width = 12)
                    ),
                    fluidRow(
                      htmlOutput("downloadInfo")
                    )
                  )
                )
)

server <- function(input, output, session) {
  
 # getmode <- function(v) {
#    uniqv <- unique(v)
 #   uniqv[which.max(tabulate(match(v, uniqv)))]
  #}
  
  observe({
    x <- input$Operator
    # To update values of the Area drop down selectInput
    updateSelectInput(session, "Area",
                      choices = as.list(unique(July[July$Operator == x , "LSA"]))
    )
    # y <- input$Area
    # updateRadioButtons(session, "Technology", label = NULL, choices = as.list(unique(July[July$Operator == x ,"Technology"])),
    #                    # selected = NULL, inline = FALSE, choiceNames = NULL, choiceValues = NULL
    #                    )
    # # 
    # updateSelectInput(session, "Technology",
    #                   choices = as.list(unique(July[July$Technology == y , "Technology"]))
    # )
  })
  
  #Preparing data for 1st histogram (Upload)
  histUp <- reactive ({
    type <- input$Type
    technology <- input$Technology
    temp <- July[ July$Operator %in% input$Operator & July$LSA %in% input$Area & July$Test_type =='upload' & July$Technology %in% technology, type]
    return(temp)
  })
  #Preparing data for 2nd histogram (Download)
  histDown <- reactive ({
    type <- input$Type
    technology <- input$Technology
    temp <- July[ July$Operator %in% input$Operator & July$LSA %in% input$Area & July$Test_type =='download' & July$Technology %in%  technology, type]
    return(temp)
  })
  #Plotting 1st histogram (Upload)
  output$histUploadplot <- renderPlot({
    Upload <- as.numeric(histUp())
    Upload <- abs(Upload)
    bins <- seq(from = min(Upload), to = max(Upload), length.out = input$Bins+1)
    hist(Upload , breaks = bins)
  })
  #Plotting 2nd histogram (Download)
  output$histDownloadplot <- renderPlot({
    Download <- as.numeric(histDown())
    Download <- abs(Download)
    bins <- seq(from = min(Download), to = max(Download), length.out = input$Bins+1)
    hist(Download , breaks = bins)
    })
  #Mean and median for the upload data
  output$uploadInfo <- renderUI({
    Upload <- as.numeric(histUp())
    Upload <- abs(Upload)
    str1 <- paste("Mean for the upload data is :")
    str2 <- paste(mean(Upload))
    str3 <- paste("<br/>")
    str4 <- paste("Median for the upload data is :")
    str5 <- paste(median(Upload))
    str6 <- paste("<br/>")
    #str7 <- paste("Mode for the upload data is :")
    #str8 <- paste(getmode(Upload))
    str9 <- paste("<br/>")
    HTML(paste(str1,str2,str3,str4,str5,str6,str9))

  })
  #Mean and median for the download data  
  output$downloadInfo <- renderUI({
    Download <- as.numeric(histDown())
    Download <- abs(Download)
    str1 <- paste("Mean for the download data is :")
    str2 <- paste(mean(Download))
    str3 <- paste("<br/>")
    str4 <- paste("Median for the download data is :")
    str5 <- paste(median(Download))
    str6 <- paste("<br/>")
    #str7 <- paste("Mode for the download data is :")
    #str8 <- paste(getmode(Download))
    str9 <- paste("<br/>")
    HTML(paste(str1,str2,str3,str4,str5,str6,str9))
  })
  
  }

shinyApp(ui = ui, server = server)
