/*
 * Copyright 2019 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
'use strict';

(function () {

    var QueryTileViewController = function ($scope, QueryService, XlrTileHelper) {
        var vm = this;
        var tile;

        var predefinedColors = [];
        predefinedColors['Undefined'] = '#7E827A';
        predefinedColors['Defined'] = '#4AA0C8';
        predefinedColors['In-Progress'] = '#FFA500';
        predefinedColors['Completed'] = '#7E8AA2';
        predefinedColors['Accepted'] = '#7FB2F0';
        predefinedColors['Production'] = '#45BF55';


        var colorPool = [
            '#B85C5A',
            '#35203B',
            '#644D52',
            '#8E2800',
            '#FF8598',
            '#FF6F69',
            '#F77A52',
            '#FCD364',
            '#FFE11A'
        ];


        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
        } else {
            // details mode
            tile = $scope.xlrTileDetailsCtrl.tile;
        }

        function tileConfigurationIsPopulated() {
            var config;
            // old style pre 7.0
            if (tile.properties == null) {
                config = tile.configurationProperties;
            } else {
                // new style since 7.0
                config = tile.properties;
            }
            return !_.isEmpty(config.server);
        }

        function getColor(value) {
            if (predefinedColors[value]) return predefinedColors[value];
            return colorPool.pop();
        }

        function getTitle(){
            if(vm.issuesSummaryData.total > 1){
                return "records";
            }
            else{
                return "record";
            }
        }

        vm.chartOptions = {
            topTitleText: function (data) {
                return data.total;
            },
            bottomTitleText: getTitle,
            series: function (data) {
                var series = {
                    name: 'ScheduleState',
                    data: []
                };
                series.data = _.map(data.data, function (value) {
                    return {y: value.counter, name: value.schedulestate, color: value.color};
                });
                return [ series ];
            },
            showLegend: false,
            donutThickness: '60%'
        };

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                QueryService.executeQuery(tile.id, config).then(
                    function (response) {
                        var ytIssueArray = [];
                        var issues = response.data.data;
                        if(issues[0] === "Invalid table name"){
                            vm.invalidTableName = true;
                        }
                        else{
                            vm.invalidTableName = false;
                            vm.states = [];
                            vm.statesCounter = 0;
                            vm.issuesSummaryData = {
                                data: null,
                                total: 0
                            };
                            vm.issuesSummaryData.data = _.reduce(issues, function (result, value) {
                                var schedulestate = value.State;
                                vm.issuesSummaryData.total += 1;
                                if (result[schedulestate]) {
                                result[schedulestate].counter += 1;
                            } else {
                                result[schedulestate] = {
                                    counter: 1,
                                    color: getColor(schedulestate),
                                    schedulestate: schedulestate
                                };
                            }
                            value.color = result[schedulestate].color;
                            ytIssueArray.push(value);
                            return result;

                        }, {});
                        _.forEach(vm.issuesSummaryData.data, function (value, key) {
                            if (vm.statesCounter < 5) vm.states.push(value);
                            vm.statesCounter++;
                        });
                        vm.gridOptions = createGridOptions(ytIssueArray);
                        }
                    }
                ).finally(function () {
                    vm.loading = false;

                });
            }
        }

        function createGridOptions(ytData) {
            var filterHeaderTemplate = "<div data-ng-include=\"'static/@project.version@/include/QueryTile/grid/name-filter-template.html'\"></div>";
            var columnDefs = [
                    {
                        displayName: "Ticket",
                        field: "id",
                        cellTemplate: "static/@project.version@/include/QueryTile/grid/id-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '10%'
                    },
                    {
                        displayName: "State",
                        field: "State",
                        cellTemplate: "static/@project.version@/include/QueryTile/grid/state-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '20%'
                    },
                    {
                        displayName: "Description",
                        field: "description",
                        cellTemplate: "static/@project.version@/include/QueryTile/grid/description-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '70%'
                    }
                ];
            return XlrTileHelper.getGridOptions(ytData, columnDefs);
        }

        function refresh() {
            load({params: {refresh: true}});
        }

        load();

        vm.refresh = refresh;
    };

    QueryTileViewController.$inject = ['$scope', 'xlrelease.yt.QueryService', 'XlrTileHelper'];

    var QueryService = function (Backend) {

        function executeQuery(tileId, config) {
            return Backend.get("/tiles/" + tileId + "/data", config);
        }
        return {
            executeQuery: executeQuery
        };
    };

    QueryService.$inject = ['Backend'];

    angular.module('xlrelease.youtrack.tile', []);
    angular.module('xlrelease.youtrack.tile').service('xlrelease.yt.QueryService', QueryService);
    angular.module('xlrelease.youtrack.tile').controller('xlrelease.yt.QueryTileViewController', QueryTileViewController);

})();
