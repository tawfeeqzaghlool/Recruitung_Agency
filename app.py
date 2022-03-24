import imp
import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Jobs, Seekers
from auth import requires_auth
import json
from flask_cors import CORS
#from auth import requires_auth
Page_count = 10
# this is for test

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_job():
        motivated = os.environ['MOTIVATED']
        job = "Full-Stack Web developer"
        if motivated == 'true':
            job = job + " This is an opportunity for you You are doing great, good luck with your search"
        return job

    @app.route('/', methods=['GET'])
    def index():
        return "<h1>Are You Ready for the new jobs?</h1>"

    #TODO get all jobs in the rectuiting web app, and just display 10 jobs per page
    @app.route('/jobs', methods=['GET'])
    @requires_auth(["get:jobs"])
    def job_all(payload):
        page = request.args.get('page', 1, type=int)
        pagination = Jobs.query.paginate(
            page, per_page=Page_count, error_out=False)
        jobs = pagination.items
        # TODO implement pagination
        # jobs = Jobs.query.all()
        jobs = [job.format() for job in jobs]
        return jsonify({'jobs': jobs, 'count': pagination.total})

    #TODO get jobs by the field in the rectuiting web app
    @app.route('/jobs/<field>', methods=['GET'])
    @requires_auth(["get:jobs"])
    def job_one(payload, field):
        job = Jobs.query.filter_by(field=field).first()
        print(field)
        # if(field not in jobs):
        if(not job):
            abort(404)
        return jsonify({'job': job.format()})
    
    #TODO get the registered seekers in the rectuiting web app, and just display 10 seekers per page
    @app.route('/seekers', methods=['GET'])
    @requires_auth(["get:seekers"])
    def seeker_all(payload):
        page = request.args.get('page', 1, type=int)
        pagination = Seekers.query.paginate(
            page, per_page=Page_count, error_out=False)
        seekers = pagination.items
        # TODO implement pagination
        # seekers = Seekers.query.all()
        seekers = [seeker.format() for seeker in seekers]
        return jsonify({'seekers': seekers, 'count': pagination.total})
    
    #TODO get seekers by their years of experience in the rectuiting web app
    @app.route('/seekers/<years_ex>', methods=['GET'])
    @requires_auth(["get:seekers"])
    def seeker_one(payload, years_ex):
        seeker = Seekers.query.filter_by(years_ex=years_ex).first()
        print(years_ex)
        # if(years_ex not in seekers):
        if(not seeker):
            abort(404)
        return jsonify({'seeker': seeker.format()})
    
    #TODO add a new job by its field in the rectuiting web app
    @app.route('/jobs', methods=['POST'])
    @requires_auth(["post:jobs"])
    def job_add(payload):
        info = request.get_json()
        if('field' not in info or 'job' not in info):
            abort(422)
        # jobs[info['field']] = info['job']
        job = Jobs(info['field'], info['job'])
        job.insert()
        return jsonify({'job': job.format()}), 201

    # TODO: implement smart job
    @app.route('/jobs/<field>/smart', methods=['POST'])
    def smart_job(payload, field):
        job = "Back_end Developer"
        return jsonify({'job': f'job in field {field} is {job}'})
    
    #TODO add a new seeker to the rectuiting web app
    @app.route('/seekers', methods=['POST'])
    @requires_auth(["post:seekers"])
    def seeker_add(payload):
        info = request.get_json()
        if('id' not in info or 'seeker' not in info):
            abort(422)
        # jobs[info['id']] = info['seeker']
        seeker = Seekers(info['id'], info['seeker'])
        seeker.insert()
        return jsonify({'seeker': seeker.format()}), 201
    
    #TODO update an existing job using its id
    @app.route('/jobs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:jobs')
    def update_job(payload, id):
    # Get the body
        req = request.get_json()
    # Get the Job with requested Id
        job = Jobs.query.filter(Jobs.id == id).one_or_none()
    # if no job with given id abort
        if not job:
            abort(404)
        try:
            req_id = req.get('id')
            req_field = req.get('field')
            # check if the id is the one is updated
            if req_id:
                job.id = req_id
            # check if the field is the one is updated
            if req_field:
                job.field = json.dumps(req['field'])
            # update the drink
            job.update()
        except Exception:
               abort(400)
        return jsonify({'success': True, 'jobs':'field'}), 200

    #TODO update an existing seeker using the id and email
    @app.route('/seekers/<int:id>', methods=['PATCH'])
    @requires_auth('patch:seekers')
    def update_seeker(payload, id):
    # Get the body
        req = request.get_json()
    # Get the Seekers with requested Id
        seeker = Seekers.query.filter(Seekers.id == id).one_or_none()
    # if no seeker with given id abort
        if not seeker:
            abort(404)
        try:
            req_id = req.get('id')
            req_email = req.get('email')
            # check if the id is the one is updated
            if req_id:
                seeker.id = req_id
            # check if the email is the one is updated
            if req_email:
                seeker.email = json.dumps(req['email'])
            # update the drink
            seeker.update()
        except Exception:
               abort(400)
        return jsonify({'success': True, 'seekers':'email'}), 200
    
    # TODO: DELETE a job using a job id
    @app.route('/jobs/<int:id>', methods=['DELETE'])
    @requires_auth('delete:jobs')
    def delete_job(id):
        '''
        Handles DELETE requests for deleting an opportunity by id.
        '''
        try:
            # get the job by id
            job = Jobs.query.filter_by(id=id).one_or_none()

            # abort 404 if no job found
            if job is None:
                abort(404)

            # delete the job
            job.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': id
            })
        except:
            # abort if problem deleting job
            abort(422)
            
    @app.route('/seekers/<int:id>', methods=['DELETE'])
    #   @requires_auth('delete:seekers')
    def delete_seeker(id):
        '''
        Handles DELETE requests for deleting a seeker by id.
        '''

        try:
            # get the seeker by id
            seeker = Seekers.query.filter_by(id=id).one_or_none()

            # abort 404 if no seeker found
            if seeker is None:
                abort(404)

            # delete the seeker
            seeker.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': id
            })

        except:
            # abort if problem deleting seeker
            abort(422)
            
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "message": "resource not found",
            "success": False,
            "error": 404,
        }), 404

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
        }), 401

    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 403,
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400


    @app.errorhandler(405)
    def method_not_allowed(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405
    @app.route('/coolkids')

    def search_well():
        return "Search well for your chance job, it's here in this app"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()