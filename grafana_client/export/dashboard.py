# ruff: noqa: ERA001, W293, T201
"""
About
=====
Python implementation of Grafana's `DashboardExporter.ts`.

State of the onion
==================
It has been started on 2022-02-15. It is a work in progress. Contributions are very much welcome!

Synopsis
========
::

    python grafana_client/model/dashboard.py play.grafana.org 000000012 | jq

Parameters
==========
- `host`: The Grafana host name to connect to.
- `dashboard uid`: The UID of the Grafana dashboard to export.

References
==========

- https://community.grafana.com/t/export-dashboard-for-external-use-via-http-api/50716
- https://github.com/panodata/grafana-client/issues/8
- https://play.grafana.org/d/000000012
"""

import dataclasses
import operator
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class AnnotationQuery:
    pass


@dataclasses.dataclass
class DashboardLink:
    pass


@dataclasses.dataclass
class PanelModel:
    pass


@dataclasses.dataclass
class Subscription:
    pass


@dataclasses.dataclass
class DashboardModel:
    """
    https://github.com/grafana/grafana/blob/v8.3.6/public/app/features/dashboard/state/DashboardModel.ts
    """

    id: Any
    uid: str
    title: str
    # autoUpdate: Any
    # description: Any
    tags: Any
    style: Any
    timezone: Any
    editable: Any
    # graphTooltip: DashboardCursorSync;
    graphTooltip: Any
    time: Any
    liveNow: bool
    # private originalTime: Any
    timepicker: Any
    templating: List[Any]
    # private originalTemplating: Any
    annotations: List[AnnotationQuery]
    refresh: Any
    # snapshot: Any
    schemaVersion: int
    version: int
    # revision: int
    links: List[DashboardLink]
    gnetId: Any
    panels: List[PanelModel]
    # panelInEdit?: PanelModel;
    # panelInView?: PanelModel;
    fiscalYearStartMonth: int
    # private panelsAffectedByVariableChange: number[] | null;
    # private appEventsSubscription: Subscription;
    # private lastRefresh: int

    # Not in dashboard payload from API, but should be exported.
    weekStart: Any = ""

    def cleanUpRepeats(self):
        pass

    def getSaveModelClone(self):
        return self

    def processRepeats(self):
        pass

    def getVariables(self):
        return self.templating["list"]

    def asdict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class DashboardExporter:
    """
    https://github.com/grafana/grafana/blob/v8.3.6/public/app/features/dashboard/components/DashExportModal/DashboardExporter.ts
    """

    inputs: Optional[List] = None
    requires: Optional[Dict] = None
    datasources: Optional[Dict] = None
    promises: Optional[List[Any]] = None
    variableLookup: Optional[Dict[str, Any]] = None
    libraryPanels: Optional[Dict[str, Any]] = None

    def makeExportable(self, dashboard: DashboardModel):
        # clean up repeated rows and panels,
        # this is done on the live real dashboard instance, not on a clone
        # so we need to undo this
        # this is pretty hacky and needs to be changed
        dashboard.cleanUpRepeats()

        saveModel = dashboard.getSaveModelClone()
        saveModel.id = None

        # undo repeat cleanup
        dashboard.processRepeats()

        self.inputs = []
        self.requires = {}
        self.datasources = {}
        self.promises = []
        self.variableLookup = {}
        self.libraryPanels = {}

        for variable in saveModel.getVariables():
            self.variableLookup[variable.name] = variable

        """
        const templateizeDatasourceUsage = (obj: any) => {
          let datasource: string = obj.datasource;
          let datasourceVariable: any = null;
        
          // ignore data source properties that contain a variable
          if (datasource && (datasource as any).uid) {
            const uid = (datasource as any).uid as string;
            if (uid.indexOf('$') === 0) {
              datasourceVariable = variableLookup[uid.substring(1)];
              if (datasourceVariable && datasourceVariable.current) {
                datasource = datasourceVariable.current.value;
              }
            }
          }
        """

        """
        promises.push(
          getDataSourceSrv()
            .get(datasource)
            .then((ds) => {
              if (ds.meta?.builtIn) {
                return;
              }
      
              // add data source type to require list
              requires['datasource' + ds.meta?.id] = {
                type: 'datasource',
                id: ds.meta.id,
                name: ds.meta.name,
                version: ds.meta.info.version || '1.0.0',
              };
      
              // if used via variable we can skip templatizing usage
              if (datasourceVariable) {
                return;
              }
      
              const refName = 'DS_' + ds.name.replace(' ', '_').toUpperCase();
              datasources[refName] = {
                name: refName,
                label: ds.name,
                description: '',
                type: 'datasource',
                pluginId: ds.meta?.id,
                pluginName: ds.meta?.name,
              };
      
              if (!obj.datasource || typeof obj.datasource === 'string') {
                obj.datasource = '${' + refName + '}';
              } else {
                obj.datasource.uid = '${' + refName + '}';
              }
            })
          );
        };
      
        const processPanel = (panel: PanelModel) => {
          if (panel.datasource !== undefined && panel.datasource !== null) {
            templateizeDatasourceUsage(panel);
          }
      
          if (panel.targets) {
            for (const target of panel.targets) {
              if (target.datasource !== undefined) {
                templateizeDatasourceUsage(target);
              }
            }
          }
      
          const panelDef: PanelPluginMeta = config.panels[panel.type];
          if (panelDef) {
            requires['panel' + panelDef.id] = {
              type: 'panel',
              id: panelDef.id,
              name: panelDef.name,
              version: panelDef.info.version,
            };
          }
        };
      
        const processLibraryPanels = (panel: any) => {
          if (isPanelModelLibraryPanel(panel)) {
            const { libraryPanel, ...model } = panel;
            const { name, uid } = libraryPanel;
            if (!libraryPanels.has(uid)) {
              libraryPanels.set(uid, { name, uid, kind: LibraryElementKind.Panel, model });
            }
          }
        };
      
        // check up panel data sources
        for (const panel of saveModel.panels) {
          processPanel(panel);
      
          // handle collapsed rows
          if (panel.collapsed !== undefined && panel.collapsed === true && panel.panels) {
            for (const rowPanel of panel.panels) {
              processPanel(rowPanel);
            }
          }
        }
      
        // templatize template vars
        for (const variable of saveModel.getVariables()) {
          if (isQuery(variable)) {
            templateizeDatasourceUsage(variable);
            variable.options = [];
            variable.current = {} as unknown as VariableOption;
            variable.refresh =
              variable.refresh !== VariableRefresh.never ? variable.refresh : VariableRefresh.onDashboardLoad;
          }
        }
      
        // templatize annotations vars
        for (const annotationDef of saveModel.annotations.list) {
          templateizeDatasourceUsage(annotationDef);
        }
        """

        # add grafana version
        self.requires["grafana"] = {
            "type": "grafana",
            "id": "grafana",
            "name": "Grafana",
            # FIXME: "version": config.buildInfo.version,
            "version": "8.4.0-beta1",
        }

        """
        return Promise.all(promises)
        .then(() => {
          each(datasources, (value: any) => {
            inputs.push(value);
          });
      
          // we need to process all panels again after all the promises are resolved
          // so all data sources, variables and targets have been templateized when we process library panels
          for (const panel of saveModel.panels) {
            processLibraryPanels(panel);
            if (panel.collapsed !== undefined && panel.collapsed === true && panel.panels) {
              for (const rowPanel of panel.panels) {
                processLibraryPanels(rowPanel);
              }
            }
          }
      
          // templatize constants
          for (const variable of saveModel.getVariables()) {
            if (isConstant(variable)) {
              const refName = 'VAR_' + variable.name.replace(' ', '_').toUpperCase();
              inputs.push({
                name: refName,
                type: 'constant',
                label: variable.label || variable.name,
                value: variable.query,
                description: '',
              });
              // update current and option
              variable.query = '${' + refName + '}';
              variable.current = {
                value: variable.query,
                text: variable.query,
                selected: false,
              };
              variable.options = [variable.current];
            }
          }
      
        })
        """

        # make inputs and requires a top thing
        newObj = dict(
            __inputs=self.inputs,
            __elements=list(self.libraryPanels.values()),
            __requires=sorted(self.requires.values(), key=operator.itemgetter("id")),
        )

        # purge some attributes.
        blocklist = ["gnetId"]
        dashboard_data = dashboard.asdict()
        for blockitem in blocklist:
            if blockitem in dashboard_data:
                del dashboard_data[blockitem]
        newObj.update(dashboard_data)

        return newObj


def main():
    import json
    import sys
    from typing import Dict

    from grafana_client import GrafanaApi
    from grafana_client.model.dashboard import DashboardExporter, DashboardModel

    def jdump(data):
        print(json.dumps(data, indent=4, sort_keys=True))

    grafana_host = sys.argv[1]
    dashboard_uid = sys.argv[2]

    # Fetch dashboard.
    grafana: GrafanaApi = GrafanaApi(None, host=grafana_host)
    dashboard_raw: Dict = grafana.dashboard.get_dashboard(dashboard_uid)
    # jdump(dashboard_raw)

    # Converge to model class.
    dashboard_data: Dict = dashboard_raw["dashboard"]
    dashboard_model: DashboardModel = DashboardModel(**dashboard_data)
    # jdump(dashboard_model.asdict())

    # Represent.
    exporter: DashboardExporter = DashboardExporter()
    exported: Dict = exporter.makeExportable(dashboard_model)
    # assert exported.templating.list[0].datasource == '${DS_GFDB}'
    jdump(exported)


if __name__ == "__main__":
    main()
