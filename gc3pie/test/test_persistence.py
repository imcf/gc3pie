#! /usr/bin/env python
#
"""
"""
# Copyright (C) 2011, GC3, University of Zurich. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
"""Test for persistency backend(s)"""

__docformat__ = 'reStructuredText'
__version__ = '$Revision$'

from gc3libs.url import Url
from gc3libs.persistence import FilesystemStore
from gc3libs.sql_persistence import SQL
import gc3libs.exceptions as gc3ex
import tempfile, os

class MyObj:
    def __init__(self, x):
        self.x = x

class MyList(list):
    """
    Add a `__dict__` to `list`, so that creating a `persistent_id`
    entry on an instance works.
    """
    pass


def _generic_persistency_test(driver):
    obj = MyObj('GC3')
    id = driver.save(obj)
    del obj
    obj = driver.load(id)
    assert obj.x == 'GC3'

    driver.remove(id)
    try:
        obj = driver.load(id)
        assert "Object %s should NOT be found" % id
    except gc3ex.LoadError:
        pass
    except Exception, e:
        raise e

def _generic_nested_persistency_test(driver):
    obj = MyList([MyObj('j1'), MyObj('j2'), MyObj('j3'), ])

    id = driver.save(obj)
    del obj
    obj = driver.load(id)
    for i in range(3):
        assert obj[i].x == 'j%d' % (i+1)

    driver.remove(id)
    try:
        obj = driver.load(id)
        assert "Object %s should NOT be found" % id
    except gc3ex.LoadError:
        pass
    except Exception, e:
        raise e

def test_file_persistency():
    path = Url('/tmp')
    fs = FilesystemStore(path.path)
    obj = MyObj('GC3')

    _generic_persistency_test(fs)
    _generic_nested_persistency_test(fs)


def test_sql_persistency():
    (fd, tmpfname) = tempfile.mkstemp()
    path = Url('sqlite://%s' % tmpfname)
    db = SQL(path)
    obj = MyObj('GC3')

    _generic_persistency_test(db)
    _generic_nested_persistency_test(db)
    os.remove(tmpfname)


def test_mysql_persistency():
    path = Url('mysql://gc3user:gc3pwd@localhost/gc3')    
    db = SQL(path)
    _generic_persistency_test(db)


def test_sql_job_persistency():
    import sqlite3
    import gc3libs
    from gc3libs.core import Run
    app = gc3libs.Application(executable='/bin/true', arguments=[], inputs=[], outputs=[], output_dir='/tmp')

    app.execution = MyObj('')
    app.execution.state = Run.State.NEW
    app.execution.lrms_jobid = 1
    app.jobname = 'GC3Test'

    (fd, tmpfname) = tempfile.mkstemp()
    path = Url('sqlite://%s' % tmpfname)
    db = SQL(path)

    id_ = db.save(app)
    
    conn = sqlite3.connect(tmpfname)
    c = conn.cursor()
    c.execute('select jobid,jobname, jobstatus from jobs')
    row = c.fetchone()
    assert int(row[0]) == app.execution.lrms_jobid
    assert row[1] == app.jobname
    assert row[2] == app.execution.state
    c.close()
    os.remove(tmpfname)
    

    
if __name__ == "__main__":
    # fix pickle error
    from test_persistence import MyObj
    test_file_persistency()
    test_sql_persistency()
    test_mysql_persistency()
    test_sql_job_persistency()