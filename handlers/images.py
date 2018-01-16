#! /usr/bin/env python
# coding: utf-8
# author:zhihua

import traceback, os, json, os, uuid
from conf import config
from base import BaseHandler


class UploadImagesHandler(BaseHandler):
    def get(self):
        self.write(config.UPLOADPAGE)

    def post(self):
        try:
            upload_path = "/Users/datagrand/test/forabbyy/ocrapi/images"
            file_metas = self.request.files.get('file', None)
            if not file_metas:
                return self.send_status_message(-2, 'invalid file content or file name.')
            meta = file_metas[0]
            fname = str(uuid.uuid1()) + os.path.splitext(meta['filename'])[1]
            with open(os.path.join(upload_path, fname), 'wb') as f:
                f.write(meta['body'])
                f.flush()
            # 转化
            os.system('cp /Users/datagrand/test/forabbyy/ocrapi/images/%s '
                      '/Users/datagrand/test/forabbyy/ocrapi/images/%s ' % (fname, os.path.splitext(fname)[0]) + '.pdf')
            if not os.path.isfile(os.path.join(upload_path, os.path.splitext(fname)[0] + '.pdf')):
                self.send_status_message(-3, 'convert to pdf failed!')
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename='+os.path.splitext(fname)[0] + '.pdf')
            with open(os.path.join(upload_path, os.path.splitext(fname)[0] + '.pdf'), 'rb') as f:
                while True:
                    data = f.read(2048)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.send_status_message(-2, traceback.format_exc())
            print traceback.format_exc()

