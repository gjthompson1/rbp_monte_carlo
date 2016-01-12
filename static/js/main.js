var exampleApp = angular.module('exampleApp',[]);

// exampleApp.config(function ($routeProvider) {
//   $routeProvider
//     .when('/', {templateUrl: 'templates/app_temp.html'})
//     .otherwise({redirectTo: '/'});
// });

exampleApp.controller('input_test', ['$scope', '$log', '$http', function($scope, $log, $http) {

    $scope.inputs  = {
      term: "36",
      loan_amount:"100000",
      int_rate:"10",
      num_loans:"1000",
      pd:"0.1",
      shape:'2'
    };

    $scope.outputs = {
      rate_cash:'100',
      RAR:'10',
      LGD:'10',
    };

    $scope.testFunc = function() {
        $log.log("input_test");
        $http.post('/calc', $scope.inputs)
  	    .then(function(response) {
    	    //  debugger;
          console.log(response.data)
           $scope.outputs = angular.copy(response.data);
  	    }, function(response) {
    	        // debugger;
  	    });
    };
}

]);
