/*
  D3InteractiveChart.js
  Author: Austin Smith, University of Maryland Libraries
  2018
*/

var input_file = "data/Combined Holdings Report.csv"

var w = 1000
var h = 450;

var country_list = d3.select("#country_list"),
    library_list = d3.select("#library_list"),
    lc_class_list = d3.select("#lc_class_list");

var chart = d3.select(".chart"),
    margin = {top: 20, right: 20, bottom: 20, left: 40},
    width = w - margin.left - margin.right,
    height = h - margin.top - margin.bottom;

var x = d3.scaleBand()
        .rangeRound([margin.left,w]);
var y = d3.scaleLinear()
        .rangeRound([h,margin.bottom]);
var y2 = d3.scaleLinear()
        .rangeRound([h,margin.bottom]);

var bar_container = chart.append("g")
  .attr("id","bar_container")
  .attr("transform","translate("+margin.left+",0)")

var circle_container = chart.append("g")
  .attr("id","circle_container")
  .attr("transform","translate("+margin.left+",0)")

var x_axis = chart.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate("+ margin.left+ "," + h + ")");

var y_axis = chart.append("g")
    .attr("class", "axis axis--y")
    .attr("transform", "translate(" + margin.left * 2 + ",0)")

var y2_axis = chart.append("g")
    .attr("class", "axis axis--y")
    .attr("transform", "translate(" + (w + margin.right * 2) + ",0)")

var x_label = chart.append("text")
  .attr("class","x_axis_label")
  .attr("transform", "translate(0"+ "," + h + ")");

var y1_label = chart.append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", 0 + margin.left)
  .attr("x",0 - (height / 2))
  .attr("dy","-1em")
  .style("text-anchor", "middle")
  .text("Holdings");

var y2_label = chart.append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", width + margin.right)
  .attr("x",0 - (height / 2))
  .attr("dy", "6.5em")
  .style("text-anchor", "middle")
  .text("Uniqueness");

var dataseries = [],
    countries = new Set(),
    libraries = new Set(),
    lc_classes = new Set();

d3.csv(input_file, function(data) {
  // Load all data into an array. Each element of array is an object
  // with properties (country, lc_class, library, data).
  // Also add countries, libraries, and classes to respective Sets.
  data.forEach(function(d) {
    var data_obj = {country:d.Country,//.toUpperCase(),
                    library:d.Library,
                    lc_class:d["LC Class"],
                    data:Object.entries(d).slice(3).map(entry => entry[1])};
    data_obj.holdings = data_obj.data.reduce((x, y) => +x + +y);
    countries.add(d.Country);//.toUpperCase());
    libraries.add(d.Library);
    lc_classes.add(d["LC Class"]);
    dataseries.push(data_obj);
    })

    country_list.selectAll("li")
        .data(Array.from(countries).sort())
      .enter().append("li")
        .attr("class","country_list_item")
        .append("input")
          .attr("checked", true)
          .attr("type","checkbox")
          .attr("class","country_selector checkbox")
          .attr("id", function(d) { return d;});

    country_list.selectAll(".country_list_item")
        .append("label")
        .text(function(d) { return d; })
        .attr("for",function(d) { return d; })

    library_list.selectAll("li")
        .data(Array.from(libraries).sort())
      .enter().append("li")
        .attr("class","library_list_item")
        .append("input")
          .attr("checked", true)
          .attr("type","checkbox")
          .attr("class","library_selector checkbox")
          .attr("id", function(d) { return d;});

    library_list.selectAll(".library_list_item")
        .append("label")
        .text(function(d) { return d; })
        .attr("for",function(d) { return d; })


    lc_class_list.selectAll("li")
        .data(Array.from(lc_classes).sort())
      .enter().append("li")
        .attr("class","lc_class_list_item")
        .append("input")
          .attr("checked", true)
          .attr("type","checkbox")
          .attr("class","lc_class_selector checkbox")
          .attr("id", function(d) { return d;});

    lc_class_list.selectAll(".lc_class_list_item")
          .append("label")
          .text(function(d) { return d; })
          .attr("for",function(d) { return d; })

    d3.selectAll(".checkbox, .series_selector").on("click", function(d){ drawChart(); });

    drawChart();
});

function drawChart() {

    // get selected parameters from each checkbox list
    var countries_selected = [];
    d3.selectAll(".country_selector").each(function(d){
      cb = d3.select(this);
      if(cb.property("checked")){
        countries_selected.push(cb.property("id"));
      }
    });
    var libraries_selected = [];
    d3.selectAll(".library_selector").each(function(d){
      cb = d3.select(this);
      if(cb.property("checked")){
        libraries_selected.push(cb.property("id"));
      }
    });
    var lc_classes_selected = [];
    d3.selectAll(".lc_class_selector").each(function(d){
      cb = d3.select(this);
      if(cb.property("checked")){
        lc_classes_selected.push(cb.property("id"));
      }
    });

    // get selected data series
    chart_category = d3.select('input[name="active_series"]:checked').node().value

    var total_holdings = new Object,
        holdings_data = new Object;
        uniqueness = new Object;

    // filter data by selected parameters
    ds = dataseries.filter(function(d) {
      return (countries_selected.includes(d.country) &&
              libraries_selected.includes(d.library) &&
              lc_classes_selected.includes(d.lc_class))
    })

    // accumulate total holdings and holdings by number of libraries for each
    //  key in chosen data series
    ds.forEach(function(entry){
        if (!(entry[chart_category] in total_holdings)) {
          total_holdings[entry[chart_category]] = 0
          holdings_data[entry[chart_category]] = new Array(entry.data.length).fill(0);
        }
        total_holdings[entry[chart_category]] += +entry.holdings
        entry.data.forEach(function(d,i){ holdings_data[entry[chart_category]][i] += +d })
    })

    // calculate uniqueness for each key in chosen data series
    Object.keys(holdings_data).forEach(function(key) {
      uniqueness[key] = 0;
      holdings_data[key].forEach(function(d,i){
         uniqueness[key] += +d / (i+1) / +total_holdings[key];
      })
    })

    x.domain(Object.keys(total_holdings).sort())
    y.domain([0, Math.max(...Object.values(total_holdings))]);
    //y2.domain([0, Math.max(...Object.values(uniqueness))]);
    y2.domain([0, 1]);

    x_axis.call(d3.axisBottom(x));
    y_axis.call(d3.axisLeft(y));
    y2_axis.call(d3.axisRight(y2));

    // add x axis
    if (chart_category == "lc_class"){ axis_name = "LC Class"
    } else { axis_name = chart_category.charAt(0).toUpperCase() + chart_category.substr(1) }
    x_label.text(axis_name);
    x_label.attr("text-anchor","middle")
    x_label.attr("transform", "translate(" + (margin.left*2 + width/2) + " ," + (height + margin.top + 20) + ")")
    x_label.attr("dy","2em")



    var bars = bar_container.selectAll("rect").data(Object.keys(total_holdings))
    var tool = d3.select("body").append("div").attr("class", "tooltip")

    bars.attr("height", d => y(0) - y(total_holdings[d]))
	      .attr("width", x.bandwidth()-3)
        .attr("x", d => x(d))
        .attr("y", d => y(total_holdings[d]))
        .on("mousemove", function (d) {
            tool.style("left", d3.event.pageX + 10 + "px")
            tool.style("top", d3.event.pageY - 20 + "px")
            tool.style("display", "inline-block")
            tool.html(total_holdings[d])
        })
        .on("mouseout", function (d) {
            tool.style("display", "none");
        })

    bars.enter().append("svg:rect")
        .attr("fill", "#0088CE")
        .attr("height", d => y(0) - y(total_holdings[d]))
	      .attr("width", x.bandwidth()-3)
        .attr("x", d => x(d))
        .attr("y", d => y(total_holdings[d]))
        .on("mousemove", function (d) {
            tool.style("left", d3.event.pageX + 10 + "px")
            tool.style("top", d3.event.pageY - 20 + "px")
            tool.style("display", "inline-block")
            tool.html(total_holdings[d])
        })
        .on("mouseout", function (d) {
            tool.style("display", "none");
        })

    bars.exit().remove()

    var symbols = circle_container.selectAll(".point")
        .data(Object.keys(uniqueness))

    symbolgen = d3.symbol().type(d3.symbolCircle).size(x.bandwidth()*2)

    symbols.attr("transform",function(d){
            xpos = x(d) + x.bandwidth()/2
            ypos = y2(uniqueness[d]) || y2(0);
            return "translate("+ xpos + "," + ypos + ")"; })
            .on("mousemove", function (d) {
                tool.style("left", d3.event.pageX + 10 + "px")
                tool.style("top", d3.event.pageY - 20 + "px")
                tool.style("display", "inline-block")
                tool.html(parseFloat(uniqueness[d]).toFixed(2))
            })
            .on("mouseout", function (d) {
                tool.style("display", "none");
            });

    symbols.enter().append("path")
      .attr("class","point")
      .attr("d",symbolgen)
      .attr("fill","gold")
      .attr("transform",function(d){
        xpos = x(d) + x.bandwidth()/2
        ypos = y2(uniqueness[d] || y2(0))
        return "translate("+ xpos + "," + ypos + ")"; })
      .on("mousemove", function (d) {
          tool.style("left", d3.event.pageX + 10 + "px")
          tool.style("top", d3.event.pageY - 20 + "px")
          tool.style("display", "inline-block")
          tool.html(parseFloat(uniqueness[d]).toFixed(2))
      })
      .on("mouseout", function (d) {
          tool.style("display", "none");
      });

    symbols.exit().remove()


}
