import ast
from textwrap import dedent

from visitor.functionDeclarationVisitor import FunctionDeclarationVisitor


class TestFunctionDeclarationVisitor:
    functionDeclarationVisitor = FunctionDeclarationVisitor()

    def assertTest(self, code, expected):
        src = dedent(code).split('\n', 1)[1]
        tree = ast.parse(src, mode='exec')
        result = self.functionDeclarationVisitor.getAllFunctionDefinitionNames(tree)
        assert result == expected

    def test_simpleDeclaration(self):
        code = '''
        def foo(): print('x')
        '''
        self.assertTest(code, {'foo'})

    def test_complexDeclaration(self):
        code = '''
        def foo(): print('x')

        x = 1
        print(len(2))
    
        def moo(): print('x')

        importedFunction(x)

        def zoo(): print('x')

        zoo(1,2,3,4)
        '''
        self.assertTest(code, {'foo', 'moo', 'zoo'})

    def test_nestedDeclarations(self):
        code = '''
        def foo():
            print('x')
            def moo():
                print('y')

                def zoo():
                    zoo()
            moo()

        '''
        self.assertTest(code, {'foo', 'moo', 'zoo'})

