

var slick = angular.module('slick', ['ngResource', 'ngSanitize', 'ui.router', 'schemaForm', 'ui.bootstrap', 'cgBusy'])
    .run(function($rootScope, $state, $stateParams, $timeout, Api, SETTINGS) {

        //console.log("sup");
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        //SETTINGS['TEMPLATE_BASE_PATH'] = '/static/slick/templates/';

        //console.log('APP_CONFIG is: ' + JSON.stringify(SETTINGS))
        /*
        // Set some configuration
        Api.Settings.get().$promise.then(function(data) {
            $rootScope.settings = data;
            $rootScope.settings['TEMPLATE_BASE_PATH'] = '/static/slick/templates/';
            Api.Apps.query().$promise.then(
                // success
                function(response) {
                    $rootScope.apps = data;
                    console.log(response);
                    //$timeout.cancel(timeoutPromise);
                }
            );
        });
        // Bit of a hack. We have to wait for everything to resolve.
        $timeout(function () {
            ready = true;
            console.log("ready");
            // Or add some error handling stuff here
        }, 2000);
        console.log("haha");
        */

    }).value('cgBusyDefaults', {
          message:'Loading Stuff',
          backdrop: true,
          delay: 300,
    });



slick.directive('pageheading', function ($rootScope, SETTINGS) {
    return {
        restrict: 'A',
        replace: true,
        templateUrl: SETTINGS['STATIC_URL'] + "slick/templates/directives/pageheading.html",
        controller: ['$scope', '$filter', function ($scope, $filter) {

        }]
    }
});

// TODO limit methods for endpoints
slick.factory("Api", function($resource) {
    return {
        Settings: $resource("/admin/api/settings/"),
        Models:  $resource("/admin/api/:app_label/:model/:pk/", { app_label: '@app_label', model: '@model', pk: '@pk'}, { 
            update: {
              method: 'PUT'
            },
            schema: {
                method: 'GET',
                isArray: false,
                url: '/admin/api/:app_label/:model/schema/',
            },
            form: {
                method: 'GET',
                isArray: true,
                url: '/admin/api/:app_label/:model/form/',
            },
        }),
        Apps: $resource("/admin/api/app/:app_label/", { app_label: '@_app_label'})
    };

});

slick.config(function ($stateProvider, $urlRouterProvider, $resourceProvider, SETTINGS) {
    $urlRouterProvider.otherwise('/');

    // TODO base on django setting
    $resourceProvider.defaults.stripTrailingSlashes = false;

    var template_base_path = SETTINGS['STATIC_URL'] + 'slick/templates/';

    $stateProvider
      .state('objects', {
        abstract: true,
        url: '/:app_label/:model',
        templateUrl: template_base_path + 'partials/objects.html',
      })
      .state('objects.list', {
        url: '',
        parent: 'objects',
        templateUrl: template_base_path + 'partials/list.html',
        controller: 'ListViewCtrl',
        /*
        views: {
            '': {
                templateUrl: template_base_path + 'partials/list.html',
                controller: 'ListViewCtrl'
            }  
        }
        */
      })
      .state('objects.list.detail', {
        parent: 'objects.list',
        url: '/:pk',
        templateUrl: template_base_path + 'partials/detail.html',
        controller: 'UpdateViewCtrl',
        resolve: {
            model: function($stateParams, Api) {
                var resource = Api.Models.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
                return resource.$promise;
            },
            schema: function($stateParams, Api) {
                var resource = Api.Models.schema({ app_label: $stateParams.app_label, model: $stateParams.model });
                return resource.$promise;
            },
            form: function($stateParams, Api) {
                var resource = Api.Models.form({ app_label: $stateParams.app_label, model: $stateParams.model });
                return resource.$promise;
            },
        },
        /*
        views: {
            'detail@objects.list': {
                templateUrl: template_base_path + 'partials/detail.html',
                controller: 'UpdateViewCtrl',

            }
        }
        */
      });

 });


slick.controller('ListViewCtrl', function($scope, $rootScope, $state, $stateParams, Api) {
    console.log("ListViewCtrl called");

    // Load apps
    Api.Apps.get({ app_label: $stateParams.app_label}, function(data) {
        $scope.app = data;
        
        angular.forEach(data['models'], function(model, key) {
            if (angular.equals(model.name, $stateParams.model)) {
                $scope.model = model;
                //console.log(model);
                $scope.page_title = model.plural;
            }
        });
    })

    Api.Models.query({ app_label: $stateParams.app_label, model: $stateParams.model}, function(data) {
        $scope.objects = data;
    })
    /*
    $scope.DetailView = function(app_label, model, id) {
        $state.go('objects.list.detail', {pk: id});
    }
    */
});


slick.controller('UpdateViewCtrl', function($scope, $stateParams, $sce, Api, model, schema, form) {
    console.log("UpdateViewCtrl called");
    //console.log(schema);
    
    $scope.model = model;
    $scope.schema = schema;
    form.push({
      type: "submit",
      title: "Save",
    });
    $scope.form = form;

    $scope.onSubmit = function(form) {
        // First we broadcast an event so all fields validate themselves
        $scope.$broadcast('schemaFormValidate');
        $scope.alerts = [];

        // Then we check if the form is valid
        if (form.$valid) {
            //console.log($scope.model);
            $scope.myPromise = $scope.model.$update({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk}).then(
                //success
                function(response) {
                    $scope.alerts.push({ type: 'success', msg: "Great success!"});
                },
                //error
                function(response) {
                    
                    // Loop through error messages
                    angular.forEach(response.data, function(value, key) {
                        angular.forEach(value, function(message, message_key) {
                            $scope.alerts.push({ type: 'danger', msg: key + ": " + message});
                        });
                    });
                    return;
                }
            );
        }
    };

});

slick.controller("SidebarController", function ($scope, $rootScope, $stateParams, Api, APPS) {
    console.log("sidebar called");

    $scope.apps = APPS;
});

