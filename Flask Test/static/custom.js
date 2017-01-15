/**
 * Created by Student on 5/01/2017.
 */

 var close, low , high, predictedclose,predictedlow,predictedhigh,closed_5day
function DrawChart (code,time) {
    var years = $("#input_Duration option:selected").text();


    var Markit = {};
    /**
     * Define the TimeseriesService.
     * First argument is symbol (string) for the quote. Examples: AAPL, MSFT, JNJ, GOOG.
     * Second argument is duration (int) for how many days of history to retrieve.
     */
    Markit.TimeseriesService = function (code, time) {
        this.symbol = code;
        this.duration = time;
        this.PlotChart();
    };

    Markit.TimeseriesService.prototype.PlotChart = function () {

        //Make JSON request for timeseries data
        $.ajax({
            beforeSend: function () {
                $("#chartDemoContainer").text("Loading chart...");
            },
            data: {
                symbol: this.symbol,
                duration: this.duration
            },
            url: "http://dev.markitondemand.com/Api/Timeseries/jsonp",
            dataType: "jsonp",
            context: this,
            success: function (json) {
                //Catch errors
                if (!json.Data || json.Message) {
                    console.error("Error: ", json.Message);
                    return;
                }
                this.BuildDataAndChart(json);
            },
            error: function () {
                alert("Couldn't generate chart.");
            }
        });
    };

    Markit.TimeseriesService.prototype.BuildDataAndChart = function (json) {
        var dateDS = json.Data.SeriesDates,
            closeDS = json.Data.Series.close.values,
            openDS = json.Data.Series.open.values,
            closeDSLen = closeDS.length,
            irregularIntervalDS = [];

        /**
         * Build array of arrays of date & price values
         * Market data is inherently irregular and HighCharts doesn't
         * really like irregularity (for axis intervals, anyway)
         */
        for (var i = 0; i < closeDSLen; i++) {
            var dat = new Date(dateDS[i]);
            var dateIn = Date.UTC(dat.getFullYear(), dat.getMonth(), dat.getDate());
            var val = closeDS[i];
            irregularIntervalDS.push([dateIn, val]);
        }

        //set dataset and chart label
        this.oChartOptions.series[0].data = irregularIntervalDS;
        this.oChartOptions.title.text = "Price History of " + json.Data.Name + "("+ years +")";

        //init chart
        new Highcharts.Chart(this.oChartOptions);
    };

    //Define the HighCharts options
    Markit.TimeseriesService.prototype.oChartOptions = {
        chart: {
            renderTo: 'chartDemoContainer'
        },
        title: {},
        subtitle: {
            text: 'Source: Thomson Reuters DataScope / Markit On Demand'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: [{ // left y axis
            title: {
                text: null
            },
            labels: {
                align: 'left',
                x: 3,
                y: 16,
                formatter: function () {
                    return Highcharts.numberFormat(this.value, 0);
                }
            },
            showFirstLabel: false
        }, { // right y axis
            linkedTo: 0,
            gridLineWidth: 0,
            opposite: true,
            title: {
                text: null
            },
            labels: {
                align: 'right',
                x: -3,
                y: 16,
                formatter: function () {
                    return Highcharts.numberFormat(this.value, 0);
                }
            },
            showFirstLabel: false
        }],
        tooltip: {
            shared: true,
            crosshairs: true
        },
        plotOptions: {
            series: {
                marker: {
                    lineWidth: 1
                }
            }
        },
        series: [{
            name: "Close price",
            lineWidth: 2,
            marker: {
                radius: 0
            }
        }]


        //,credits:{ enabled:false },
    };
    new Markit.TimeseriesService(code, time);



}
var code;
$(function() {

    $("#symbolsearch")
        .focus()
        .autocomplete({
            source: function(request,response) {
                $.ajax({
                    beforeSend: function(){
                        $("span.help-inline").show();
                        $("span.label-info").empty().hide();
                    },
                    url: "http://dev.markitondemand.com/api/v2/Lookup/jsonp",
                    dataType: "jsonp",
                    data: {
                        input: request.term
                    },
                    success: function(data) {
                        response( $.map(data, function(item) {
                            return {
                                label: item.Name + " (" +item.Exchange+ ")",
                                value: item.Symbol
                            }
                        }));
                        $("span.help-inline").hide();

                    }
                });
            },
            minLength: 0,
            select: function( event, ui ) {
                code = ui.item.value;

//                            console.log(ui.item);
//                            $("ui-helper-hidden-accessible").style.display="none";
                $("span.label-info").html("You selected " + ui.item.label).fadeIn("fast");

            }
        })
    ;
//

});

function sendData(code,time){


//  code : code on the financial market , company symbol
//  time : the amount of days of the financial hisotory request

var details = {
    "code" : code,
    "time" : time
}

    $.ajax({
        url: "/receiveData",
        type:"POST",
        data: JSON.stringify(details,null,'\t'),
        contentType:"application/json; charset=utf-8",
        success : function(response){
                value = JSON.parse(response)

                var closed_1day = value.data_closed1day
                var closed_2day = value.data_closed2day
                var closed_3day = value.data_closed3day
                var closed_4day = value.data_closed4day
                var closed_5day = value.data_closed5day
                var dataPredict_high = value.data_predictHigh
                var dataPredict_low = value.data_predictlow
                var current = value.currentValue
                predictedhigh = dataPredict_high
                predictedlow = dataPredict_low
                predictedclose = closed_5day

                close_4day()


                if(parseFloat(closed_1day)<parseFloat(current))
                {

                     var trToday = document.getElementById("close_Today")
                     trToday.innerHTML ="+"
                     trToday.style.color="green"
                     trToday.style.fontSize="25px"
                }
                else {

                var trToday = document.getElementById("close_Today")
                     trToday.innerHTML ="-"
                     trToday.style.color="red"
                     trToday.style.fontSize="25px"
                }
                 if(parseFloat(closed_2day)<parseFloat(closed_1day))
                {

                     var trToday = document.getElementById("close_1day")
                     trToday.innerHTML ="+"
                     trToday.style.color="green"
                     trToday.style.fontSize="25px"
                }
                else {

                var trToday = document.getElementById("close_1day")
                     trToday.innerHTML ="-"
                     trToday.style.color="red"
                     trToday.style.fontSize="25px"
                }

                  if(parseFloat(closed_3day)<parseFloat(closed_2day))
                {

                     var trToday = document.getElementById("close_2day")
                     trToday.innerHTML ="+"
                     trToday.style.color="green"
                     trToday.style.fontSize="25px"
                }
                else {

                var trToday = document.getElementById("close_2day")
                     trToday.innerHTML ="-"
                     trToday.style.color="red"
                     trToday.style.fontSize="25px"
                }
                  if(parseFloat(closed_4day)<parseFloat(closed_3day))
                {

                     var trToday = document.getElementById("close_3day")
                     trToday.innerHTML ="+"
                     trToday.style.color="green"
                     trToday.style.fontSize="25px"
                }
                else {

                var trToday = document.getElementById("close_3day")
                     trToday.innerHTML ="-"
                     trToday.style.color="red"
                     trToday.style.fontSize="25px"
                }
                    if(parseFloat(closed_5day)<parseFloat(closed_4day))
                {

                     var trToday = document.getElementById("close_4day")
                     trToday.innerHTML ="+"
                     trToday.style.color="green"
                     trToday.style.fontSize="25px"
                }
                else {

                var trToday = document.getElementById("close_4day")
                     trToday.innerHTML ="-"
                     trToday.style.color="red"
                     trToday.style.fontSize="25px"
                }
                var trToday = document.getElementById("today")
                var trTomorrow = document.getElementById("+1day")
                trToday.innerHTML = (value.currentValue).toFixed(4)
                close = value.predictedclose0;
                high = value.pricehigh;
                low = value.pricelow
                setTimeout(showPrediction,1000)

                function showPrediction(){
                if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
                {

                trTomorrow.innerHTML ="+"
                trTomorrow.style.color="green"
                trTomorrow.style.fontSize="25px"
                }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }}
                console.log(response)

        },
        error: function(error){
            console.log("Error")
        }
    })
}

function get_2day(){
    var details = {
        "close": close,
        "high" :high,
        "low" :low
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            close = value.predictedclose0
            low = value.pricelow
            high = value.pricehigh

            var trTomorrow = document.getElementById("+2day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)


        },
        error: function(error){
            console.log("Error")
        }
    })
}

function get_3day(){
    var details = {
        "close": close,
        "high" :high,
        "low" :low
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            close = value.predictedclose0
            low = value.pricelow
            high = value.pricehigh

            var trTomorrow = document.getElementById("+3day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)


        },
        error: function(error){
            console.log("Error")
        }
    })
}

function get_4day(){
    var details = {
        "close": close,
        "high" :high,
        "low" :low
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            close = value.predictedclose0
            low = value.pricelow
            high = value.pricehigh

            var trTomorrow = document.getElementById("+4day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)


        },
        error: function(error){
            console.log("Error")
        }
    })
}

function close_4day(){
    var details = {
        "close": predictedclose,
        "high" :predictedhigh,
        "low" :predictedlow
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            predictedclose = value.predictedclose0
            predictedlow = value.pricelow
            predictedhigh = value.pricehigh

            var trTomorrow = document.getElementById("predicted_4day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)
            close_3day()
        },
        error: function(error){
            console.log("Error")
        }
    })
}
function close_3day(){
    var details = {
        "close": predictedclose,
        "high" :predictedhigh,
        "low" :predictedlow
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            predictedclose = value.predictedclose0
            predictedlow = value.pricelow
            predictedhigh = value.pricehigh

            var trTomorrow = document.getElementById("predicted_3day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)
            close_2day()


        },
        error: function(error){
            console.log("Error")
        }
    })
}

function close_2day(){
    var details = {
        "close": predictedclose,
        "high" :predictedhigh,
        "low" :predictedlow
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            predictedclose = value.predictedclose0
            predictedlow = value.pricelow
            predictedhigh = value.pricehigh

            var trTomorrow = document.getElementById("predicted_2day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)
            close_1day()


        },
        error: function(error){
            console.log("Error")
        }
    })
}
function close_1day(){
    var details = {
        "close": predictedclose,
        "high" :predictedhigh,
        "low" :predictedlow
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            predictedclose = value.predictedclose0
            predictedlow = value.pricelow
            predictedhigh = value.pricehigh

            var trTomorrow = document.getElementById("predicted_1day")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)
            close_Today()


        },
        error: function(error){
            console.log("Error")
        }
    })
}

function close_Today(){
    var details = {
        "close": predictedclose,
        "high" :predictedhigh,
        "low" :predictedlow
    }
    $.ajax({
        url: "/getNextDay",
        data: JSON.stringify(details,null,'\t'),
        type:"POST",
        contentType:"application/json; charset=utf-8",
        success : function(response){
            value = JSON.parse(response)
            predictedclose = value.predictedclose0
            predictedlow = value.pricelow
            predictedhigh = value.pricehigh

            var trTomorrow = document.getElementById("predicted_Today")

            setTimeout(showPrediction,1000)
            function showPrediction(){
            if(parseFloat(value.predictedclose0)>parseFloat(value.currentValue))
             {
              trTomorrow.innerHTML ="+"
              trTomorrow.style.color="green"
              trTomorrow.style.fontSize="25px"
             }else {
                trTomorrow.innerHTML = "-"
                trTomorrow.style.color="red"
                trTomorrow.style.fontSize = "25px";
                }
            }
            console.log(response)


        },
        error: function(error){
            console.log("Error")
        }
    })
}