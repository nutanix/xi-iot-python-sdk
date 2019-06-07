from __future__ import absolute_import

import logging
import uuid
import sys
import time
logging.basicConfig( stream=sys.stderr, format='%(funcName)s:%(levelname)s:%(message)s', level=logging.DEBUG )

import xiiot_api
from xiiot_api.api.application_api import ApplicationApi
from xiiot_api.rest import ApiException

XI_IOT_ENDPOINT='https://iot.nutanix.com'
USER_EMAIL = ""
USER_PWD = ""

class ApplicationApiWrapper():
    """ApplicationApi Test Class"""

    def __init__(self, xi_iot_endpoint, userEmail, userPwd):
        self.configuration, _ = self.loginUsingAuthTag(xi_iot_endpoint, userEmail, userPwd)
        self.authorization = self.configuration.get_api_key_with_prefix('Authorization')

        self.api_client = xiiot_api.ApiClient(configuration=self.configuration)

        self.ApplicationApi = xiiot_api.api.application_api.ApplicationApi(api_client=self.api_client)
        self.AppStatusApi = xiiot_api.api.application_status_api.ApplicationStatusApi(api_client=self.api_client)
        self.ProjectApi = xiiot_api.ProjectApi(api_client=self.api_client)
        self.EdgeApi = xiiot_api.api.edge_api.EdgeApi(api_client=self.api_client)  

    def loginUsingAuthTag(self, xi_iot_endpoint, userEmail, userPwd):
        configuration = xiiot_api.Configuration()
        configuration.host = xi_iot_endpoint
        api_client = xiiot_api.ApiClient(configuration=configuration)

        # create an instance of the API class
        api_instance = xiiot_api.AuthApi(api_client=api_client)
        request = xiiot_api.Credential(userEmail, userPwd)

        try:
            # Lets the user log in.
            api_response = api_instance.login_call_v2(request)

            # Configure API key authorization: BearerToken
            configuration.api_key['Authorization'] = api_response.token
            configuration.api_key_prefix['Authorization'] = 'Bearer'
            configuration.debug = False

            return configuration, api_response

        except ApiException as e:
            logging.error("Exception when calling AuthApi->login_call_v2: %s", e)
            raise

    def create_application(self, app_name, app_manifest, project_id, edge_ids):
        # ApplicationV2 | Describes the application creation request.
        body = xiiot_api.ApplicationV2(name=app_name, app_manifest=app_manifest, project_id=project_id, edge_ids=edge_ids)

        try:
            api_response = self.ApplicationApi.application_create_v2(body, self.authorization)
            # returns CreateDocumentResponseV2 object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_create_v2: %s", e)
            raise

    def delete_application(self, app_id):
        
        try:
            api_response = self.ApplicationApi.application_delete_v2(self.authorization, app_id)
            # returns DeleteDocumentResponseV2 object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationApi->application_create_v2: %s", e)
            raise

    def get_projects(self, project_name=None):

        try:
            if project_name is not None:
                # int | 0-based index of the page to fetch results. (optional)
                page_index = 0
                page_size = 100  # int | Item count of each page. (optional)
                # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
                # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)
                filter = "name = \'%s\'" % project_name

                api_response = self.ProjectApi.project_list_v2(
                    self.authorization, page_index=page_index, page_size=page_size, filter=filter)
            else:
                api_response = self.ProjectApi.project_list_v2(self.authorization)
            # returns ProjectListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ProjectApi->project_list_v2: %s",e)
            raise

    def get_applications_statuses(self, app_id=None):
        try:
            if app_id is not None:
                api_response = self.AppStatusApi.application_status_get_v2(
                    self.authorization, app_id)
            else:
                api_response = self.AppStatusApi.application_status_list_v2(self.authorization)
            logging.info("application_status_list_v2 API output: %s" % api_response)
            # returns ApplicationStatusListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ApplicationStatusApi->application_status_list/get_v2: %s", e)
            raise

    def get_edges(self):
        # page_index = 789 # int | 0-based index of the page to fetch results. (optional)
        # page_size = 789 # int | Item count of each page. (optional)
        # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
        # filter = 'filter_example' # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)

        try:
            #api_response = api_instance.edge_list_v2(authorization, page_index=page_index, page_size=page_size, order_by=order_by, filter=filter)
            api_response = self.EdgeApi.edge_list_v2(self.authorization)
            logging.info("edge_list API output: %s" % api_response)
            # returns EdgeListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Edgepi->edge_list_v2: %s", e)
            raise

    def project_get_edges(self, project_id):
        # page_index = 789 # int | 0-based index of the page to fetch results. (optional)
        # page_size = 789 # int | Item count of each page. (optional)
        # order_by = ['order_by_example'] # list[str] | Specify result order. Zero or more entries with format: &ltkey> [desc] where orderByKeys lists allowed keys in each response. (optional)
        # filter = 'filter_example' # str | Specify result filter. Format is similar to a SQL WHERE clause. For example, to filter object by name with prefix foo, use: name LIKE 'foo%'. Supported filter keys are the same as order by keys. (optional)

        try:
            #api_response = api_instance.edge_list_v2(authorization, page_index=page_index, page_size=page_size, order_by=order_by, filter=filter)
            api_response = self.EdgeApi.project_get_edges_v2(project_id, self.authorization)
            logging.info("edge_list API output: %s" % api_response)
            # returns EdgeListPayload object
            return api_response
        except ApiException as e:
            logging.error("Exception when calling Edgepi->project_get_edges_v2: %s", e)
            raise

def main():
    """Test application_create_v2  and application_delete_v2 APIs
    """
    app_api_wrapper = ApplicationApiWrapper(XI_IOT_ENDPOINT, USER_EMAIL, USER_PWD)

    PROJECT_NAME="Default Project"
    logging.info("Getting id of project: %s", PROJECT_NAME)
    projectListPayload = app_api_wrapper.get_projects(PROJECT_NAME)

    for project in projectListPayload.result:
        logging.info("%s project id: %s", PROJECT_NAME, project.id)
        project_id = project.id
        break

    app_name = "flask-web-server-blog"
    with open("./flask-web-server.yaml", "r") as yamlFile:
        app_manifest = yamlFile.read()

    edgeListPayload = app_api_wrapper.project_get_edges(project_id)
    edge_ids = []
    for edge in edgeListPayload.result:
        logging.info("edge name: %s | edge serial number: %s" % (edge.name, edge.serial_number))
        edge_ids.append(edge.id)

    #This test does not pass project_id as its documented as optional
    logging.info("Creating flask-web-server app...")
    createDocumentResponseV2 = app_api_wrapper.create_application(app_name, app_manifest, project_id, edge_ids)
    logging.info("Created application with id: %s", createDocumentResponseV2.id)

    time.sleep(60)
    logging.info("Getting app status for app id: %s...", createDocumentResponseV2.id)
    applicationStatusListPayload = app_api_wrapper.get_applications_statuses(createDocumentResponseV2.id)
    logging.info("Received app status for app id: %s", createDocumentResponseV2.id)

    logging.info("Deleteing application with id: %s...", createDocumentResponseV2.id)
    deleteDocumentResponseV2 = app_api_wrapper.delete_application(createDocumentResponseV2.id)
    logging.info("Deleted application with id: %s", deleteDocumentResponseV2.id)

if __name__ == "__main__":
  main()