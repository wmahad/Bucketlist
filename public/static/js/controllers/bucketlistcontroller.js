'use strict';


app.controller('BucketListController',
    function BucketListController($rootScope, $scope, $state, $localStorage, $stateParams, BucketListService, toastr) {
        $('.modal-trigger').leanModal();
        var BlService = BucketListService;

        $scope.username = $localStorage.currentUser;

        //get bucketlist data
        $scope.Bucketlists = BlService.Bucketlists.getAllBuckets();
        $scope.$on('updateBucketData', function () {
            $scope.Bucketlists = BucketListService.Bucketlists.getAllBuckets();
        });

        $scope.openModal = function(bucketlist_id) {
            $scope.bucketedit = BlService.Bucketlists.getOneBucket({
                id: bucketlist_id
            });
            $('#modal1').openModal();
        };

        //create a new bucketlist
        $scope.createBucketlist = function() {
            var data = {
                name: $scope.newbucket.name
            };
            BlService.Bucketlists.createBucket(data)
                .$promise
                .then(function(response) {
                    $scope.newbucket.name = null
                    $scope.$emit('updateBucketData');
                    toastr.success('Bucketlist created successfully');
                })
                .catch(function(responseError) {
                    toastr.error('Bucketlist not created');
                });

        };

        //update bucketlist
        $scope.updateBucketlist = function(_id) {
            var data = {
                name: $scope.bucketedit.name,
                id: _id
            };
            console.log(data);
            BlService.Bucketlists.updateBucket(data)
                .$promise
                .then(function(response) {
                    $scope.bucketedit.name = null
                    $scope.$emit('updateBucketData');
                    $('#modal1').closeModal();
                    toastr.success('Bucketlist updated successfully');
                })
                .catch(function(responseError) {
                    toastr.error('Bucketlist not updated');
                });

        };

        //delete individual bucketlist
        $scope.deleteBucketlist = function(bucket) {
            bucket.$deleteBucket().then(function() {
                $scope.$emit('updateBucketData');
                toastr.success('Bucketlist deleted successfully');
            });
        };
    }
);



app.controller('BucketListViewController',
    function BucketListViewController($rootScope, $scope, $state, $localStorage, $stateParams, BucketListService, toastr) {
        $('.modal-trigger').leanModal();
        $scope.$on('updateData', function () {
            $scope.BucketlistItem = BucketListService.Bucketlists.getOneBucket({
                id: $stateParams.id
            });
        });

        $scope.username = $localStorage.currentUser;
        $scope.BucketlistItem = BucketListService.Bucketlists.getOneBucket({
            id: $stateParams.id
        });

        $scope.openItemModal = function(bucketlist_id, item_id) {
            var data = {
                bid: bucketlist_id,
                id: item_id
            };
            $scope.itemedit = BucketListService.BucketlistItems.getOneBucketItem(data);
            $('#modal1').openModal();
        };

        $scope.createBucketItem = function(url_params) {
            BucketListService.BucketlistItems.createBucketItem(url_params)
                .$promise
                .then(
                    function(response) {
                        $scope.newitem.name = null
                        $scope.$emit('updateData');
                        toastr.success('Item created successfully');
                    })
                .catch(function(responseError) {
                    toastr.error('Item not created');
                });
        };

        $scope.deleteItem = function(url_params) {
            BucketListService.BucketlistItems.deleteBucketItem(url_params)
                .$promise
                .then(
                    function(response) {
                        $scope.$emit('updateData');
                        toastr.success('Item deleted successfully');
                    }
                );
        };

        $scope.editItem = function(_id, b_id) {
            var data = {
                name: $scope.itemedit.name,
                id: _id,
                bucketlist: b_id,
                bid: b_id
            };
            BucketListService.BucketlistItems.updateBucketItem(data)
                .$promise
                .then(
                    function(response) {
                        $scope.itemedit.name = null;
                        $scope.$emit('updateData');
                        $('#modal1').closeModal();
                        toastr.success('Item updated successfully');
                    }
                );
        };


        $scope.toggleCompleted = function(item, _id, b_id) {
            var data = {
                done: item.done,
                name: item.name,
                id: _id,
                bucketlist: b_id,
                bid: b_id
            };
            BucketListService.BucketlistItems.updateBucketItem(data)
                .$promise
                .then(
                    function(response) {
                        toastr.success('Item updated successfully');
                    }
                );
        }

    }
);
