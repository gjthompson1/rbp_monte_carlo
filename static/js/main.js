var exampleApp = angular.module('exampleApp',[]);

// exampleApp.config(function ($routeProvider) {
//   $routeProvider
//     .when('/', {templateUrl: 'templates/app_temp.html'})
//     .otherwise({redirectTo: '/'});
// });

exampleApp.controller('FormController1',function($scope){
        $scope.buttonClicked = function(){
            $scope.modText = $scope.inputText;
        };
    });

exampleApp.controller('input_test', ['$scope', '$log', '$http', function($scope, $log, $http) {

    $scope.inputs  = {term: "36"};
    $scope.returnVal = 100;

    $scope.testFunc = function() {
        $log.log("input_test");
        $http.post('/calc', $scope.inputs)
  	    .then(function(response) {
    	    //  debugger;
           $scope.returnVal = angular.copy(response.data.mult_val);
  	    }, function(response) {
    	        // debugger;
  	    });
    };
}

]);

// exampleApp.calculateRiskPricing: function($scope.inputs) {
//     var payload = {
//         inputs: inputs
//     };
//     return httpService.call('/app_temp', payload);
// },
