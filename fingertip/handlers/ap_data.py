# -*- coding: utf-8 -*-

from tornado import web
import json
from services import fingertip
from helpers import db
from models.ap_data import APData

class APDataHandler(web.RequestHandler):
    def post(self):
        current_fingertip = fingertip.service.current_fingertip

        if current_fingertip is not None and not current_fingertip.is_outdated():
            self.set_status(400, reason='Fingertip gone or outdated.')
            self.finish()

        if self.request.body is None:
            self.set_status(400, reason='Empty body.')
            self.finish()

        try:
            body = json.loads(self.request.body.decode('utf-8'))
            APData(body).save()

        except json.decoder.JSONDecodeError as e:
            self.set_status(400, reason='Error parsing JSON.')
        except db.DBException as e:
            self.set_status(500, reason=e.message)
